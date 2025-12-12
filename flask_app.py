from flask import Flask, render_template, redirect, request
from build_llm_message import build_defender_message, build_attacker_message
from llm_communication import send_message_to_openai, send_message_to_gemini
from check_query import is_query_safe
from attack import attack, columns as result_type
from pathlib import Path
import os
import datetime
import database
import markdown

app = Flask(__name__)

def format_db_table(db_response):

    # string plain text
    if isinstance(db_response, str):
        return f"<pre>{db_response}</pre>"

    # list of dicts
    if isinstance(db_response, list) and len(db_response) > 0 and isinstance(db_response[0], dict):
        headers = db_response[0].keys()
        rows = [
            "<tr>" + "".join(f"<th>{h}</th>" for h in headers) + "</tr>"
        ]

        for row in db_response:
            rows.append("<tr>" + "".join(f"<td>{row[h]}</td>" for h in headers) + "</tr>")

        return "<table class='table table-striped table-sm'>" + "".join(rows) + "</table>"

    return "<pre>No data</pre>"

def run_query():

    # ----------------------------------------------------
    # PHASE 2 — User will decide if database was breached
    # ----------------------------------------------------
    if "decision" in request.form:
        user_vote = request.form["decision"]
        user_query = request.form["user_query"]
        db_response = request.form["db_response"]

        try:
            message_llm = build_defender_message(user_query, db_response)

            llm_output_gemini = send_message_to_gemini(message_llm)
            llm_output_openai = send_message_to_openai(message_llm)

        except Exception as e:
            error_msg = f"### LLM Error\n```\n{e}\n```"
            return markdown.markdown(error_msg), False, { "title": "", "text": "", "original_query": "" }

        #get time where response was generated
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Create the file and the folder if not existing
        script_dir = Path(__file__).parent
        log_folder = script_dir / "logs_user_querries"
        os.makedirs(log_folder, exist_ok=True)
        filename = os.path.join(log_folder, f"response_{timestamp}.txt")

        # Write both the message and response to the log file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("### Executed Querry\n" + user_query + "\n" + "### LLM Responses\n" + "######**OpenAI:**\n" + llm_output_openai + "\n" + "######**Gemini:**\n" + llm_output_gemini + "\n" + "### User Judgment\n" + "Breached? " + user_vote.upper())


        return markdown.markdown("### Executed Querry\n" + user_query + "\n" + "### LLM Responses\n" + "######**OpenAI:**\n" + llm_output_openai + "\n" + "######**Gemini:**\n" + llm_output_gemini + "\n" + "### User Judgment\n" + "Breached? " + user_vote.upper()), False, {"title": "","text": "","original_query": ""}

    # --------------------------------------------------
    # PHASE 1 — User submitted SQL query
    # --------------------------------------------------
    user_query = request.form["query"]

    try:
        database.sanitize_query(user_query)
        db_response = database.execute_query(user_query)

        table_html = format_db_table(db_response)

        db_response_md = markdown.markdown(f"```\n{db_response}\n```")

        # show the modular review box
        return db_response_md, True, {
            "title": "Does this query actually breach?",
            "text": table_html,
            "original_query": user_query
        }

    except Exception as e:
        return f"<h3>Error:</h3> {e}", False, {"title": "","text": "","original_query": ""}



def run_simulation():
    attacker = request.form['attacker']
    defender = request.form['defender']
    count = int(request.form['count'])

    results = attack(attacker, defender, count)

    output = ""
    for result in results:
        if result == result_type.BREACH_RIGHT.value:
            output += "The defender correctly determined the query was a breach.<br>"
        elif result == result_type.BREACH_WRONG.value:
            output += "The defender incorrectly said the query was a breach.<br>"
        elif result == result_type.NO_BREACH_RIGHT.value:
            output += "The defender correctly determined the query was not a breach.<br>"
        elif result == result_type.NO_BREACH_WRONG.value:
            output += "The defender incorrectly said the query was a breach.<br>"

    return output

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

    #manual running of querries
    if request.method == "POST" and (request.form.get("query") or request.form.get("decision")):
        output, show_review, extra = run_query()
        return render_template("queries.html", llm_response=output, show_review=show_review, **extra)

    # SIMULATION mode
    elif request.method == "POST":
        output = run_simulation()
        return render_template("queries.html", llm_response=output, show_review=False)

    # get and blank page
    return render_template("queries.html", llm_response="", show_review=False)

@app.route('/contact')
def contact():
    return render_template("contact.html")

if __name__ == '__main__':
    app.run(ssl_context='adhoc')
