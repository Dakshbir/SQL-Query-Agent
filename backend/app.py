
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
load_dotenv()
logging.basicConfig(level=logging.INFO)

# Enhanced NLTK setup with error handling
def setup_nltk():
    """Setup NLTK with proper error handling and retries"""
    try:
        # Ensure NLTK data directory exists
        nltk_data_dir = '/root/nltk_data'
        if not os.path.exists(nltk_data_dir):
            os.makedirs(nltk_data_dir, exist_ok=True)
        
        # Download required packages with retries
        packages = ['stopwords', 'punkt']
        for package in packages:
            try:
                nltk.data.find(f'tokenizers/{package}')
                logging.info(f"NLTK package {package} already available")
            except LookupError:
                logging.info(f"Downloading NLTK package: {package}")
                nltk.download(package, quiet=True)
                time.sleep(1)  # Brief pause between downloads
        
        # Verify punkt tokenizer is working
        from nltk.tokenize import sent_tokenize
        test_text = "This is a test sentence. This is another sentence."
        sentences = sent_tokenize(test_text)
        logging.info(f"NLTK tokenizer test successful: {len(sentences)} sentences")
        
        return True
    except Exception as e:
        logging.error(f"NLTK setup failed: {e}")
        return False

# Initialize NLTK with retries
nltk_ready = False
for attempt in range(3):
    if setup_nltk():
        nltk_ready = True
        break
    else:
        logging.warning(f"NLTK setup attempt {attempt + 1} failed, retrying...")
        time.sleep(2)

if not nltk_ready:
    logging.error("Failed to initialize NLTK after 3 attempts")

# Initialize RAKE only if NLTK is ready
rake = None
if nltk_ready:
    try:
        rake = Rake()
        logging.info("RAKE initialized successfully")
    except Exception as e:
        logging.error(f"RAKE initialization failed: {e}")
                          # keyword extractor

# ------------------------------------------------------------------#
#  2. FLASK APP INIT                                                #
# ------------------------------------------------------------------#
app = Flask(__name__)

CORS(app, origins=[
    "http://localhost:3000",
    "http://localhost:5173",
    "https://sql-query-agent.vercel.app",  # Your exact Vercel URL
    "https://*.vercel.app"  # Fallback for other Vercel deployments
])                     # allow any front-end

# ------------------------------------------------------------------#
#  3. DATABASE UTILS (uses database.py from your repo)              #
# ------------------------------------------------------------------#
from database import list_all_tables, get_table_schema
_schema_cache: dict | None = None

# Get DATABASE_URL from environment variables
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
    """Extract relevant schema based on natural language input with error handling"""
    try:
        if rake is None:
            logging.warning("RAKE not available, using fallback schema")
            schema = load_db_schema()
            return "\n".join(f"Table {t} columns: {', '.join(c)}" for t, c in schema.items())
        
        # Use RAKE for keyword extraction
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
    except Exception as e:
        logging.error(f"Error in relevant_schema: {e}")
        # Fallback: return all schema
        schema = load_db_schema()
        return "\n".join(f"Table {t} columns: {', '.join(c)}" for t, c in schema.items())

def ask_groq(prompt: str) -> str | None:
    try:
        resp = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=500,
        )
        return resp.choices.message.content  # ✅ access first choice

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
        database_ready=bool(DATABASE_URL),
        nltk_ready=nltk_ready,
        rake_ready=rake is not None,
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


# ------------------------------------------------------------------#
#  6. ROOT ROUTE (for Railway deployment)                          #
# ------------------------------------------------------------------#
@app.route("/", methods=["GET"])
def root():
    """Root endpoint to provide basic API information"""
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
        },
        "documentation": "Visit the frontend application to use the SQL Query Agent"
    })



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
