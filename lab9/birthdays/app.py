import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

# Configure sessions
app.secret_key = 'bce9dd7334dbd1ad321082ef134874effca3d5960389e6e05118ae3f1dd10172'


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # TODO: Add the user's entry into the database

        # Processing the input
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")

        session['name'] = name
        session['month'] = month
        session['day'] = day

        # Validate submission
        if not name or not month or not day:
            return redirect(url_for("failure"))

        # Insert into db
        db.execute(
            "INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)", name, month, day)

        return redirect(url_for("index"))

    else:

        # TODO: Display the entries in the database on index.html
        entries = db.execute("SELECT * FROM birthdays")

        return render_template("index.html", entries=entries)


@ app.route("/remove", methods=["POST"])
def remove():

    # Remove ID
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM birthdays WHERE id = ? ", id)
    return redirect(url_for("index"))


@ app.route("/failure")
# Route if failure arises
def failure():
    name = session.get('name', None)
    month = session.get('month', None)
    day = session.get('day', None)
    return render_template("failure.html", name=name, month=month, day=day)
