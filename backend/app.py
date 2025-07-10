import os
import json
import time
import logging
import sqlparse
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from rake_nltk import Rake
import nltk

# ------------------------------------------------------------------#
#  1. ENV & LIB SET-UP                                              #
# ------------------------------------------------------------------#
load_dotenv()                                    # reads .env
logging.basicConfig(level=logging.INFO)

# ensure stop-words are available for RAKE
try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")
    nltk.download("punkt")          # RAKE needs Punkt tokenizer too

# Groq ≥ 0.28 fixes the “proxies” bug, so plain init works
from groq import Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

rake = Rake()                                   # keyword extractor

# ------------------------------------------------------------------#
#  2. FLASK APP INIT                                                #
# ------------------------------------------------------------------#
app = Flask(__name__)
CORS(app, origins=[
    "http://localhost:3000",  # local development
    "http://localhost:5173",  # vite dev server
    "https://your-app-name.vercel.app",  # production frontend (update after deployment)
    "https://*.vercel.app"  # all vercel apps for testing
])                       # allow any front-end

# ------------------------------------------------------------------#
#  3. DATABASE UTILS (uses database.py from your repo)              #
# ------------------------------------------------------------------#
from database import list_all_tables, get_table_schema
_schema_cache: dict | None = None


def load_db_schema(force_reload: bool = False) -> dict:
    global _schema_cache
    if _schema_cache and not force_reload:
        return _schema_cache

    db_conf = {
        'db_name': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),  # This was missing!
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT')
    }
    
    schema: dict[str, list[str]] = {}
    for table in list_all_tables(**db_conf):
        cols = get_table_schema(table_name=table, **db_conf)
        schema[table] = list(cols.keys())

    _schema_cache = schema
    return schema


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
    rake.extract_keywords_from_text(nl)
    kw = {k.lower() for k in rake.get_ranked_phrases()}
    schema = load_db_schema()
    pieces = []
    for tbl, cols in schema.items():
        if kw & ({tbl.lower()} | {c.lower() for c in cols}):
            pieces.append(f"Table {tbl} columns: {', '.join(cols)}")
    return "\n".join(pieces) or "\n".join(
        f"Table {t} columns: {', '.join(c)}" for t, c in schema.items()
    )


def ask_groq(prompt: str) -> str | None:
    try:
        resp = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=500,
        )
        return resp.choices[0].message.content  # ✅ access first choice

    except Exception as e:
        logging.error("Groq API error: %s", e)
        return None


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
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify(
        status="ok",
        groq_ready=bool(client.api_key),
        timestamp=time.time(),
    )


@app.route("/api/schema", methods=["GET"])
def schema():
    refresh = request.args.get("refresh") == "true"
    return jsonify(schema=load_db_schema(refresh), success=True)


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