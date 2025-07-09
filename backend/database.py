import psycopg2
from psycopg2 import sql
import os

def create_tables_from_sql_file(sql_file_path, db_name, user, password, host='localhost', port='5432'):
    # Connect to PostgreSQL server
    conn = psycopg2.connect(dbname=db_name, user=user, password=password, host=host, port=port)
    conn.autocommit = True
    cursor = conn.cursor()

    # Read SQL file
    with open(sql_file_path, 'r', encoding='utf-8') as file:
        sql_commands = file.read()

    # Execute SQL commands
    # Split commands and execute each separately
    sql_statements = sql_commands.split(';')
    for statement in sql_statements:
        # Skip empty statements
        if statement.strip():
            try:
                cursor.execute(sql.SQL(statement))
                print(f"Successfully executed statement.")
            except Exception as e:
                print(f"Error executing statement: {e}")
                print(f"Failed statement: {statement[:100]}...")
                continue
    print("Finished executing all SQL commands.")
    
    cursor.close()
    conn.close()

# List all tables
def list_all_tables(db_name, user, password, host='localhost', port='5432'):
    conn = psycopg2.connect(dbname=db_name, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    tables = cursor.fetchall()
    cursor.close()
    conn.close()
    return [table[0] for table in tables]

# Get table schema - FIXED: Using parameterized query to prevent SQL injection
def get_table_schema(db_name, user, password, host='localhost', port='5432', table_name=''):
    conn = psycopg2.connect(dbname=db_name, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()
    cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = %s", (table_name,))
    columns = cursor.fetchall()
    cursor.close()
    conn.close()
    return {col[0]: col[1] for col in columns}

# Function to delete all tables - FIXED: Using proper SQL identifiers
def delete_all_tables(db_name, user, password, host='localhost', port='5432'):
    conn = psycopg2.connect(dbname=db_name, user=user, password=password, host=host, port=port)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
    tables = cursor.fetchall()
    
    for table in tables:    
        cursor.execute(sql.SQL("DROP TABLE IF EXISTS {} CASCADE").format(sql.Identifier(table[0])))
        print(f"Dropped table: {table[0]}")
        print(" -------------------------------- ")
        
    # List of enums you wish to delete
    enums_to_delete = [
        'wishlist_status_enum',
        'priority_level_enum',
        'added_from_source_enum'
    ]
    
    for enum in enums_to_delete:
        cursor.execute(sql.SQL("DROP TYPE IF EXISTS {}").format(sql.Identifier(enum)))
        print(f"Dropped enum: {enum}")
        print(" -------------------------------- ")
        
    cursor.close()
    conn.close()

if __name__ == "__main__":
    # Define your database connection parameters
    db_name = 'postgres'
    user = 'postgres'
    password = 'Daksh@0708'
    
    # Use relative paths for the SQL files
    schema_file_path = os.path.join(os.path.dirname(__file__), "sample_database_schema.sql")
    data_file_path = os.path.join(os.path.dirname(__file__), "sample_data.sql")

    print("Creating database schema...")
    create_tables_from_sql_file(schema_file_path, db_name, user, password)
    
    print("\nInserting sample data...")
    create_tables_from_sql_file(data_file_path, db_name, user, password)
    
    print("\nListing all tables:")
    tables = list_all_tables(db_name, user, password)
    for table in tables:
        print(f"- {table}")
    
    print(f"\nTotal tables created: {len(tables)}")
