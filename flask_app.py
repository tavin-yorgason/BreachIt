from flask import Flask, render_template, redirect, url_for, request
import mysql.connector
from build_llm_message import build_llm_message
from llm_communication import send_message_to_llm
from dotenv import load_dotenv
import os

from pathlib import Path

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)

# ----------------------
# SQL Communication
# ----------------------
def get_db_connection():
    return mysql.connector.connect(
        host = os.getenv("DB_HOST"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        database = os.getenv("DB_NAME")
    )

def execute_query(user_query):
    """
    Executes a SQL query and returns the results.
    SELECT queries return list of dicts; other queries return a summary string.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(user_query)
        if user_query.strip().lower().startswith("select"):
            columns = [c[0] for c in cursor.description]
            rows = cursor.fetchall()
            result = [dict(zip(columns, r)) for r in rows]
        else:
            conn.commit()
            result = f"{cursor.rowcount} rows affected"
    finally:
        conn.close()
    return result

@app.route('/run_query', methods=['POST'])
def run_query():
    user_query = request.form['query']

    try:
        db_response = execute_query(user_query)
        
        # Build message and send to LLM
        message_llm = build_llm_message(user_query, db_response)
        llm_output = send_message_to_llm(message_llm)

        return f"<h3>LLM Output:</h3><pre>{llm_output}</pre>"

    except Exception as e:
        return f"<h3>Error:</h3> {e}"

@app.route('/')
def default():
    return redirect("/home")

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/queries')
def queries():
    return render_template("queries.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

if __name__ == '__main__':
    app.run(ssl_context='adhoc')
