from flask import Flask, render_template, redirect, url_for, request
import mysql.connector
from build_llm_message import build_llm_message
from llm_communication import send_message_to_llm
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# ----------------------
# SQL Communication
# ----------------------
def get_db_connection():
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_name = os.getenv("DB_NAME")

    print(f"username: {db_user} | password: {db_pass} | host: {db_host} | name: {db_name}")

    return mysql.connector.connect(
        host=db_host,
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

@app.route('/run_query', methods=['POST'])
def run_query():
    user_query = request.form['query']

    try:
        print("about to call exec query")
        db_response = execute_query(user_query)
        
        print("hellooooooooooooooooooooooooooo")

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
    app.logger.error("This is an error message")
    return render_template("queries.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

if __name__ == '__main__':
    app.run(ssl_context='adhoc')
