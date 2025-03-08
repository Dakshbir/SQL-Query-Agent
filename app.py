import os
import json
import time
import logging
import asyncio
import sqlparse
import numpy as np
from dotenv import load_dotenv
from flask import Flask, jsonify
from database import list_all_tables, get_table_schema
from groq import Groq
from sentence_transformers import SentenceTransformer
from rake_nltk import Rake

load_dotenv()
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
model = SentenceTransformer("all-MiniLM-L6-v2")
r = Rake()

with open('train_generate_task.json', 'r') as f:
    nl_to_sql_examples = json.load(f)

with open('train_query_correction_task.json', 'r') as f:
    query_correction_examples = json.load(f)

schema_cache = {}

def load_db_schema():
    if "schema_context" in schema_cache:
        return schema_cache["schema_context"]
    
    schema_context = {}
    tables = list_all_tables(os.getenv("DB_NAME"), os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_HOST"), os.getenv("DB_PORT"))
    for table in tables:
        columns = get_table_schema(os.getenv("DB_NAME"), os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_HOST"), os.getenv("DB_PORT"), table)
        schema_context[table] = list(columns.keys())
    
    schema_cache["schema_context"] = schema_context
    return schema_context

def get_relevant_schema(nl_query):
    r.extract_keywords_from_text(nl_query)
    keywords = set(r.get_ranked_phrases())
    schema_context = load_db_schema()
    
    filtered_schema = ""
    for table, columns in schema_context.items():
        if any(keyword in table.lower() or keyword in " ".join(columns).lower() for keyword in keywords):
            filtered_schema += f"Table {table} columns: {', '.join(columns)}\n"
    
    return filtered_schema if filtered_schema else "\n".join([f"Table {table} columns: {', '.join(columns)}" for table, columns in schema_context.items()])

def is_valid_sql(query):
    try:
        parsed = sqlparse.parse(query)
        return bool(parsed)
    except:
        return False

def call_groq_api(prompt):
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="mixtral-8x7b-32768",
            temperature=0,
            max_tokens=500,
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Groq API Error: {e}")
        return None

def generate_sql_from_nl(nl_query):
    schema_context = get_relevant_schema(nl_query)
    prompt = f"""
You are an expert SQL assistant. Given the database schema below:

{schema_context}

Translate this natural language query into SQL accurately:

NL: {nl_query}
SQL:
"""
    for attempt in range(3):
        generated_sql = call_groq_api(prompt)
        if generated_sql and is_valid_sql(generated_sql):
            clean_sql = generated_sql.replace("\\", "")  # Remove unnecessary backslashes
            print(f"✅ Generated SQL (cleaned): {clean_sql}")
            return clean_sql
        time.sleep(2 ** attempt)
    print("❌ SQL Generation Failed after retries")
    return None

async def generate_sql_async(nl_query):
    return await asyncio.to_thread(generate_sql_from_nl, nl_query)

@app.route('/generate_submission', methods=['GET'])
async def generate_submission():
    with open('sample_submission_generate_task.json', 'r') as f:
        submission_tasks = json.load(f)

    tasks = [generate_sql_async(task["NL"]) for task in submission_tasks]
    results = await asyncio.gather(*tasks)
    
    final_submission = []
    for task, sql in zip(submission_tasks, results):
        clean_sql = sql.replace("\\", "") if sql else "Generation Failed"
        final_submission.append({"NL": task["NL"], "Query": clean_sql})
        print(f"✅ Final Submission (cleaned): {clean_sql}")
    
    with open('final_submission_generate_task.json', 'w') as outfile:
        json.dump(final_submission, outfile, indent=2)
    
    return jsonify({
      "message": "Submission file generated successfully!",
      "submission_file": "final_submission_generate_task.json",
      "results": final_submission
    })

@app.route('/generate_query_correction_submission', methods=['GET'])
async def generate_query_correction_submission():
    with open('sample_submission_query_correction_task.json', 'r') as f:
        correction_tasks = json.load(f)

    # Ensure the correct key is used
    valid_tasks = [task for task in correction_tasks if "IncorrectQuery" in task]

    if not valid_tasks:
        return jsonify({"error": "No valid IncorrectQuery entries found in input file"}), 400

    tasks = [generate_sql_async(task["IncorrectQuery"]) for task in valid_tasks]
    results = await asyncio.gather(*tasks)

    final_submission = []
    for task, corrected_sql in zip(valid_tasks, results):
        if corrected_sql:
            clean_corrected_sql = corrected_sql.replace("\\", "")
            final_submission.append({
                "IncorrectQuery": task["IncorrectQuery"],
                "CorrectQuery": clean_corrected_sql
            })
            print(f"✅ Corrected (cleaned): {clean_corrected_sql}")
        else:
            final_submission.append({
                "IncorrectQuery": task["IncorrectQuery"],
                "CorrectQuery": "Correction Failed"
            })
            print("❌ Correction Failed after retries")

    with open('final_submission_query_correction_task.json', 'w') as outfile:
        json.dump(final_submission, outfile, indent=2)

    return jsonify({
        "message": "Query correction submission file generated successfully!",
        "submission_file": "final_submission_query_correction_task.json",
        "results": final_submission
    })


if __name__ == "__main__":
    app.run(debug=True)