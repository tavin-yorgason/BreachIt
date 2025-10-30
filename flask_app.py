from flask import Flask, render_template, redirect, url_for, request
from build_llm_message import build_llm_message
from llm_communication import send_message_to_llm
import database
import markdown
import os

app = Flask(__name__)

def run_query():
    user_query = request.form['query']

    try:
        db_response = database.execute_query(user_query)
        
        # Build message and send to LLM
        message_llm = build_llm_message(user_query, db_response)
        llm_output = send_message_to_llm(message_llm)

        return markdown.markdown(llm_output)

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
