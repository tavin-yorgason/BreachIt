from flask import Flask, render_template, redirect, request
from build_llm_message import build_defender_message, build_attacker_message
from llm_communication import send_message_to_openai, send_message_to_gemini
from check_query import is_query_safe
import database
import markdown

app = Flask(__name__)

def run_query():
    user_query = request.form['query']

    try:
        database.sanitize_query(user_query)
        db_response = database.execute_query(user_query)

        is_safe = is_query_safe(user_query)
        breaches = not is_safe

        # Build message and send to LLM
        message_llm = build_defender_message(user_query, db_response)
        llm_output = send_message_to_gemini(message_llm)

        return markdown.markdown(llm_output +
            "\n### Does the query actually breach?\n" +
            "Yes" if breaches else
            llm_output + "\n#### Does the query actually breach?\n" + "No")

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
