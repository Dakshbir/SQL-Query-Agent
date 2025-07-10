import os
import json
import time
import logging
import sqlparse
import re
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

# ------------------------------------------------------------------#
#  1. ENV & LIB SET-UP                                              #
# ------------------------------------------------------------------#
load_dotenv()
logging.basicConfig(level=logging.INFO)

# Remove NLTK/RAKE imports and initialization
# from rake_nltk import Rake
# import nltk

# Simple keyword extraction without NLTK
def extract_keywords(text):
    """Simple keyword extraction without NLTK dependencies"""
    # Convert to lowercase and split into words
    words = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', text.lower())
    
    # Common SQL/database stop words to filter out
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
        'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after',
        'above', 'below', 'between', 'among', 'all', 'any', 'both', 'each', 'few', 'more',
        'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
        'than', 'too', 'very', 'can', 'will', 'just', 'should', 'now', 'show', 'me', 'get',
        'find', 'list', 'display', 'give', 'tell', 'what', 'where', 'when', 'how', 'why',
        'who', 'which', 'that', 'this', 'these', 'those', 'i', 'you', 'he', 'she', 'it',
        'we', 'they', 'them', 'their', 'there', 'here', 'is', 'are', 'was', 'were', 'be',
        'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'done'
    }
    
    # Filter out stop words and return unique keywords
    keywords = [word for word in words if word not in stop_words and len(word) > 2]
    return list(set(keywords))

# Groq client initialization
from groq import Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ------------------------------------------------------------------#
#  2. FLASK APP INIT                                                #
# ------------------------------------------------------------------#
app = Flask(__name__)
CORS(app, origins=[
    "http://localhost:3000",
    "http://localhost:5173",
    "https://sql-query-agent.vercel.app"
])

# ------------------------------------------------------------------#
#  3. DATABASE UTILS                                                #
# ------------------------------------------------------------------#
from database import list_all_tables, get_table_schema
_schema_cache: dict | None = None

DATABASE_URL = os.getenv("DATABASE_URL")

def load_db_schema(force_reload: bool = False) -> dict:
    global _schema_cache
    if _schema_cache and not force_reload:
        return _schema_cache

    if not DATABASE_URL:
        logging.error("DATABASE_URL is not set. Cannot load schema.")
        return {}
    
    schema: dict[str, list[str]] = {}
    try:
        tables = list_all_tables(DATABASE_URL)
        for table in tables:
            cols = get_table_schema(DATABASE_URL, table_name=table)
            schema[table] = list(cols.keys())
        
        _schema_cache = schema
        return schema
    except Exception as e:
        logging.error(f"Error loading database schema: {e}")
        return {}

# ------------------------------------------------------------------#
#  4. HELPERS                                                       #
# ------------------------------------------------------------------#
def clean_markdown_sql(text: str | None) -> str | None:
    """strip ``````sql code fences and backslashes"""
    if not text:
        return None
    txt = text.replace("\\", "").strip()
    if txt.startswith("```sql"):
        txt = txt[6:]
    elif txt.startswith("```"):
        txt = txt[3:]

    if txt.endswith("```"):
        txt = txt[:-3]
    return txt.strip()

def relevant_schema(nl: str) -> str:
    """Extract relevant schema using simple keyword matching"""
    try:
        # Use simple keyword extraction instead of RAKE
        keywords = extract_keywords(nl)
        schema = load_db_schema()
        pieces = []
        
        for tbl, cols in schema.items():
            # Check if any keyword matches table name or column names
            table_keywords = {tbl.lower()} | {c.lower() for c in cols}
            if any(keyword in table_keywords for keyword in keywords):
                pieces.append(f"Table {tbl} columns: {', '.join(cols)}")
        
        # If no specific matches, return all schema (fallback)
        return "\n".join(pieces) or "\n".join(
            f"Table {t} columns: {', '.join(c)}" for t, c in schema.items()
        )
    except Exception as e:
        logging.error(f"Error in relevant_schema: {e}")
        # Ultimate fallback: return all schema
        schema = load_db_schema()
        return "\n".join(f"Table {t} columns: {', '.join(c)}" for t, c in schema.items())

def ask_groq(prompt: str) -> str | None:
    """Make request to Groq API with proper error handling"""
    try:
        resp = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=500,
        )
        
        # Correct way to access the response
        if resp.choices and len(resp.choices) > 0:
            return resp.choices[0].message.content
        else:
            logging.error("No choices in Groq API response")
            return None

    except Exception as e:
        logging.error(f"Groq API error: {e}")
        return None

def load_db_schema(force_reload: bool = False) -> dict:
    """Load database schema with proper error handling"""
    global _schema_cache
    if _schema_cache and not force_reload:
        return _schema_cache

    if not DATABASE_URL:
        logging.error("DATABASE_URL is not set. Cannot load schema.")
        return {}
    
    schema: dict[str, list[str]] = {}
    try:
        tables = list_all_tables(DATABASE_URL)
        for table in tables:
            cols = get_table_schema(DATABASE_URL, table_name=table)
            schema[table] = list(cols.keys())
        
        _schema_cache = schema
        logging.info(f"Successfully loaded schema with {len(schema)} tables")
        return schema
    except Exception as e:
        logging.error(f"Error loading database schema: {e}")
        return {}



def nl_to_sql(nl: str) -> str | None:
    schema_txt = relevant_schema(nl)
    prompt = (
        "You are an expert SQL assistant. Given the database schema below:\n\n"
        f"{schema_txt}\n\n"
        f"Translate this natural-language request into SQL.\n\nNL: {nl}\nSQL:"
    )

    for attempt in range(3):
        raw = ask_groq(prompt)
        sql = clean_markdown_sql(raw)
        if sql and sqlparse.parse(sql):
            return sql
        time.sleep(2 ** attempt)
    return None

def fix_sql(bad_sql: str) -> str | None:
    prompt = (
        "You are an expert SQL assistant. Correct the following query and "
        "return valid SQL only.\n\nIncorrect SQL:\n"
        f"{bad_sql}\n\nCorrected SQL:"
    )
    for attempt in range(3):
        raw = ask_groq(prompt)
        sql = clean_markdown_sql(raw)
        if sql and sqlparse.parse(sql):
            return sql
        time.sleep(2 ** attempt)
    return None

# ------------------------------------------------------------------#
#  5. ENDPOINTS                                                     #
# ------------------------------------------------------------------#
@app.route("/", methods=["GET"])
def root():
    return jsonify({
        "message": "SQL Query Agent API is running",
        "status": "online",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/health",
            "schema": "/api/schema", 
            "generate_sql": "/api/generate-sql",
            "correct_sql": "/api/correct-sql",
            "validate_sql": "/api/validate-sql"
        }
    })

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify(
        status="ok",
        groq_ready=bool(client.api_key),
        database_ready=bool(DATABASE_URL),
        nltk_free=True,  # Indicate we're not using NLTK
        timestamp=time.time(),
    )

@app.route("/api/schema", methods=["GET"])
def schema():
    refresh = request.args.get("refresh") == "true"
    schema_data = load_db_schema(refresh)
    return jsonify(schema=schema_data, success=True)

@app.route("/api/generate-sql", methods=["POST"])
def gen_sql():
    nl = request.json.get("query", "").strip()
    if not nl:
        return jsonify(success=False, error="Query is empty"), 400
    sql = nl_to_sql(nl)
    if not sql:
        return jsonify(success=False, error="Failed to generate SQL"), 500
    return jsonify(success=True, sql=sql, nl_query=nl)

@app.route("/api/correct-sql", methods=["POST"])
def corr_sql():
    bad_sql = request.json.get("query", "").strip()
    if not bad_sql:
        return jsonify(success=False, error="SQL is empty"), 400
    sql = fix_sql(bad_sql)
    if not sql:
        return jsonify(success=False, error="Failed to correct SQL"), 500
    return jsonify(success=True, corrected_sql=sql, original_sql=bad_sql)

@app.route("/api/validate-sql", methods=["POST"])
def validate():
    q = request.json.get("query", "").strip()
    if not q:
        return jsonify(success=False, error="SQL is empty"), 400
    is_valid = bool(sqlparse.parse(q))
    return jsonify(
        success=True,
        is_valid=is_valid,
        formatted_sql=sqlparse.format(q, reindent=True, keyword_case="upper"),
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
