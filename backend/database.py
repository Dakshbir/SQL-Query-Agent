import os
import psycopg2
from dotenv import load_dotenv

# This will load environment variables from a .env file if it exists.
# It's great for local development and does nothing in production if the file is absent.
load_dotenv()

def execute_sql_from_file(sql_file_path, db_url):
    """
    Connects to the database using the provided URL and executes an entire SQL script.
    
    Args:
        sql_file_path (str): The path to the .sql file.
        db_url (str): The full database connection URL.
    """
    if not db_url:
        print("Error: DATABASE_URL is not set. Cannot execute SQL.")
        return

    try:
        # Establish a connection using the database URL
        conn = psycopg2.connect(db_url)
        # Use autocommit to ensure each command is executed immediately
        conn.autocommit = True
        cursor = conn.cursor()

        with open(sql_file_path, 'r', encoding='utf-8') as file:
            # Read the entire file content. This is more robust than splitting by ';'.
            sql_script = file.read()
            if sql_script.strip():  # Ensure the script is not empty
                cursor.execute(sql_script)
                print(f"Successfully executed script from: {os.path.basename(sql_file_path)}")

        cursor.close()
        conn.close()

    except FileNotFoundError:
        print(f"Error: The file {sql_file_path} was not found.")
    except Exception as e:
        print(f"An error occurred while executing {os.path.basename(sql_file_path)}: {e}")

def list_all_tables(db_url):
    """
    Lists all tables in the public schema of the database.
    
    Args:
        db_url (str): The full database connection URL.
        
    Returns:
        list: A list of table names.
    """
    tables = []
    if not db_url:
        print("Error: DATABASE_URL is not set. Cannot list tables.")
        return tables
        
    try:
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        # Query to get all table names from the public schema
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        tables = [table for table in cursor.fetchall()]
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"An error occurred while trying to list tables: {e}")
        
    return tables

def get_table_schema(db_url, table_name=''):
    """
    Gets the schema (column names and data types) for a specific table.
    
    Args:
        db_url (str): The full database connection URL.
        table_name (str): The name of the table to get schema for.
        
    Returns:
        dict: A dictionary mapping column names to their data types.
    """
    schema = {}
    if not db_url:
        print("Error: DATABASE_URL is not set. Cannot get table schema.")
        return schema
        
    try:
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = %s ORDER BY ordinal_position", 
            (table_name,)
        )
        columns = cursor.fetchall()
        schema = {col: col for col in columns}
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"An error occurred while getting schema for table {table_name}: {e}")
        
    return schema

def delete_all_tables(db_url):
    """
    Deletes all tables and custom types from the database.
    
    Args:
        db_url (str): The full database connection URL.
    """
    if not db_url:
        print("Error: DATABASE_URL is not set. Cannot delete tables.")
        return
        
    try:
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        
        # Drop all tables with CASCADE
        for table in tables:    
            cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
            print(f"Dropped table: {table}")
            
        # List of enums to delete
        enums_to_delete = [
            'wishlist_status_enum',
            'priority_level_enum',
            'added_from_source_enum'
        ]
        
        # Drop custom types
        for enum in enums_to_delete:
            cursor.execute(f"DROP TYPE IF EXISTS {enum}")
            print(f"Dropped enum: {enum}")
            
        cursor.close()
        conn.close()
        print("All tables and enums deleted successfully.")
        
    except Exception as e:
        print(f"An error occurred while deleting tables: {e}")

# This block will only run when you execute the script directly (e.g., `python database.py`)
if __name__ == "__main__":
    # Get the single, powerful database connection URL from environment variables.
    # This is the most important change for compatibility with Railway.
    DATABASE_URL = os.getenv("DATABASE_URL")

    # Check if the DATABASE_URL is actually set
    if not DATABASE_URL:
        print("CRITICAL ERROR: The DATABASE_URL environment variable is not set.")
        print("Please go to your backend service variables in Railway and add it.")
        print("The value should be: ${{ Postgres.DATABASE_URL }}")
    else:
        # Construct full, OS-independent paths to your SQL files
        base_dir = os.path.dirname(__file__)
        schema_file_path = os.path.join(base_dir, "sample_database_schema.sql")
        data_file_path = os.path.join(base_dir, "sample_data.sql")

        print("--- Starting Database Setup ---")

        print("\nStep 1: Creating database schema...")
        execute_sql_from_file(schema_file_path, DATABASE_URL)

        print("\nStep 2: Inserting sample data...")
        execute_sql_from_file(data_file_path, DATABASE_URL)

        print("\nStep 3: Verifying created tables...")
        tables_found = list_all_tables(DATABASE_URL)
        
        if tables_found:
            for table in tables_found:
                print(f"- {table}")
            print(f"\nSUCCESS: Found {len(tables_found)} tables in the database.")
        else:
            print("VERIFICATION FAILED: No tables were found in the database.")
        
        print("\n--- Database Setup Complete ---")
