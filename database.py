import mysql.connector
from dotenv import load_dotenv
import os
from pathlib import Path

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path = env_path)

def get_connection():
    return mysql.connector.connect(
        host = os.getenv("DB_HOST"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        database = os.getenv("DB_NAME")
    )

def execute_queries(queries):
    query = ""
    for line in queries.splitlines():
        query += line
        
        if line.endswith(";"):
            execute_query(query)
            query = ""

def execute_query(query):
    """
    Executes a SQL query and returns the results.
    SELECT queries return list of dicts; other queries return a summary string.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        if query.strip().lower().startswith("select"):
            columns = [c[0] for c in cursor.description]
            rows = cursor.fetchall()
            result = [dict(zip(columns, r)) for r in rows]
        else:
            conn.commit()
            result = f"{cursor.rowcount} rows affected"
    finally:
        conn.close()
    return result
