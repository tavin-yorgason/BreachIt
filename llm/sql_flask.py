from flask import Flask, request, render_template
import mysql.connector
from build_llm_message import build_llm_message
from llm_communication import send_message_to_llm
import os

app = Flask(__name__)

# ----------------------
# SQL Communication
# ----------------------
def get_db_connection():
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_name = os.getenv("DB_NAME")

    return mysql.connector.connect(
        host=db_host,                   #change to the IP so everyone can use it need to be adjusted depending where we are
        user=db_user,
        password=db_pass,
        database=db_name
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

@app.route('/')
def index():
    return render_template('queries.html')

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

if __name__ == '__main__':
    app.run(debug=True)
