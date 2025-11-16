from flask import Flask, render_template, redirect, url_for, request
from build_llm_message import build_llm_message
#from llm_communication_gemini import send_message_to_llm
from llm_communication_openai import send_message_to_llm
import database
import markdown
import os

app = Flask(__name__)

bad_sql_keywords = [
    'insert', 'update', 'delete',
    'replace', 'drop', 'alter', 'truncate'
]

def run_query():
    user_query = request.form['query']

    try:
        bad_keyword_used = contains_any(user_query, bad_sql_keywords)
        if bad_keyword_used != "":
            raise Exception("Database-altering SQL keyword used: " \
                            f"{bad_keyword_used}")

        db_response = database.execute_query(user_query)

        # Build message and send to LLM
        message_llm = build_llm_message(user_query, db_response)
        llm_output = send_message_to_llm(message_llm)

        return markdown.markdown(llm_output)

    except Exception as e:
        return f"<h3>Error:</h3> {e}"

def contains_any(string, substrings):
    for substring in substrings:
        if substring in string.lower():
            return substring
    
    return ""

@app.route('/')
def default():
    return redirect("/home")

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/queries', methods = ["GET", "POST"])
def queries():
    output = ""

    if request.method == "POST":
        output = run_query()

    return render_template("queries.html", llm_response = output)

@app.route('/contact')
def contact():
    return render_template("contact.html")

if __name__ == '__main__':
    app.run(ssl_context='adhoc')
