import os
import mysql.connector
from enum import Enum
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path = env_path)

bad_sql_keywords = [
    'insert', 'update', 'delete',
    'replace', 'drop', 'alter', 'truncate'
]

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
        columns = [c[0] for c in cursor.description]
        rows = cursor.fetchall()
        result = [dict(zip(columns, r)) for r in rows]
    finally:
        conn.close()
    return result

def sanitize_query(query):
    bad_keyword = first_contained_in(query.lower(), bad_sql_keywords)
    if bad_keyword != "":
        raise Exception("Database-altering SQL keyword used: {bad_keyword}")

def first_contained_in(string, substrings):
    for substring in substrings:
        if substring in string:
            return substring

    return ""
