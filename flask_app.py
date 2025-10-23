from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

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
