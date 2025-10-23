from flask import Flask, request, render_template_string
import mysql.connector
from build_llm_message import build_llm_message
from llm_communication import send_message_to_llm

app = Flask(__name__)

# ----------------------
# SQL Communication
# ----------------------
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="flask_user",
        password="strongpassword",
        database="flask_db"
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

# ----------------------
# Flask Routes
# ----------------------
html_form = """
<h2>SQL Query Tester</h2>
<form action="/run_query" method="post">
    <input type="text" name="query" placeholder="Enter SQL query" size="80">
    <input type="submit" value="Run Query">
</form>
"""

@app.route('/')
def index():
    return render_template_string(html_form)

@app.route('/run_query', methods=['POST'])
def run_query():
    user_query = request.form['query']
    db_setup = "Describe your database schema here (tables, columns, etc.)"

    try:
        db_response = execute_query(user_query)

        # Build message and send to LLM
        message_llm = build_llm_message(db_setup, user_query, db_response)
        llm_output = send_message_to_llm(message_llm)

        return f"<h3>LLM Output:</h3><pre>{llm_output}</pre>"

    except Exception as e:
        return f"<h3>Error:</h3> {e}"

if __name__ == '__main__':
    app.run(debug=True)
