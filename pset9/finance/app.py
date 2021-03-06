import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show portfolio of stocks"""
    # Process the buy/sell requests on POST:
    if request.method == "POST":

        # Send the request to the appropriate place when buying
        symbol = request.form.get("symbol")
        if request.form.get("type") == "Buy":
            return render_template("buy.html", symbol=symbol)

        # Send the request to the appropriate place when selling
        elif request.form.get("type") == "Sell":
            # also query the transactions to fill up the dropdown selector
            transactions = db.execute("SELECT symbol AS symbol, name AS name, SUM(shares) AS shares, price, SUM(shares * price) AS stock_total FROM transactions WHERE user_id = ? GROUP BY symbol",
                                      session["user_id"])
            return render_template("sell.html", transactions=transactions, symbol=symbol)
        else:
            redirect("/")

    # Show the overview with a GET request
    else:

        # Query all transactions for the user
        transactions = db.execute("SELECT symbol AS symbol, name AS name, SUM(shares) AS shares, price, SUM(shares * price) AS stock_total FROM transactions WHERE user_id = ? GROUP BY symbol",
                                  session["user_id"])

        # Lookup current prices
        total = 0
        for transaction in transactions:
            transaction["price"] = lookup(transaction["symbol"])["price"]
            total += (transaction["price"] * transaction["shares"])

        # Query for the amount of cash of the user
        cash = db.execute("SELECT cash FROM users WHERE id = ?",
                          session["user_id"])

        return render_template("index.html", transactions=transactions, total=total, cash=cash[0]["cash"])


@ app.route("/buy", methods=["GET", "POST"])
@ login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        # Get variables
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Ensure symbol was submitted
        if not symbol:
            return apology("must provide symbol", 400)

        # Ensure shares was submitted
        if not shares:
            return apology("must provide amount of shares", 400)

        # Ensure whole shares are submitted
        if not shares.isdigit():
            return apology("must provide whole number of shares", 400)

        # Ensure positive amount of shares was submitted
        if int(shares) <= 0:
            return apology("must provide a positive amount of shares", 400)

        stock = lookup(request.form.get("symbol"))

        if stock == None:
            return apology("stock doesn't exist", 400)

        # Ensure the user has enough cash to make the purchase
        amount = int(shares) * stock["price"]

        row = db.execute("SELECT cash FROM users WHERE id = ?",
                         session["user_id"])
        cash = row[0]["cash"]
        if cash < amount:
            return apology("you do not have enough money to buy these shares", 400)

        # Process transaction into transactions database
        db.execute("INSERT INTO transactions (symbol, shares, price, name, user_id) VALUES (?, ?, ?, ?, ?)",
                   symbol, int(shares), stock["price"], stock["name"], session["user_id"],)

        # Update cash field in users database
        cash_after = cash - amount
        db.execute("UPDATE users SET cash = ? WHERE id = ?",
                   cash_after, session["user_id"])

        return redirect("/")

    else:
        return render_template("buy.html", symbol=None)


@ app.route("/history")
@ login_required
def history():
    """Show history of transactions"""
    # Query all transactions for the user
    transactions = db.execute(
        "SELECT * FROM transactions WHERE user_id = ? ORDER BY date_time", session["user_id"])
    return render_template("history.html", transactions=transactions)


@ app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@ app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@ app.route("/quote", methods=["GET", "POST"])
@ login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":

        # Check if symbol has been provided
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("no symbol provided", 400)

        # Using the lookup function to lookup the stock
        stock = lookup(symbol)

        # Check if stock has been found
        if stock == None:
            return apology("stock doesn't exist", 400)

        # Return the stock information
        return render_template("quoted.html", name=stock["name"], price=stock["price"], symbol=stock["symbol"])
    else:
        return render_template("quote.html")


@ app.route("/quoted", methods=["POST"])
@ login_required
def quoted():
    """Include a buy button from the quoted page"""

    # Process the buy/sell requests on POST:
    if request.method == "POST":
        symbol = request.form.get("symbol")

        # Send the request to the appropriate place when buying
        if request.form.get("type") == "Buy":
            return render_template("buy.html", symbol=symbol)

        # Send the request to the appropriate place when selling
        elif request.form.get("type") == "Sell":
            # also query the transactions to fill up the dropdown selector
            transactions = db.execute("SELECT symbol AS symbol, name AS name, SUM(shares) AS shares, price, SUM(shares * price) AS stock_total FROM transactions WHERE user_id = ? GROUP BY symbol",
                                      session["user_id"])
            return render_template("sell.html", transactions=transactions, symbol=symbol)
    else:
        return redirect("/quote")


@ app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Process the input
        username = request.form.get("username")
        password = generate_password_hash(request.form.get("password"))
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        if not password:
            return apology("must provide password", 400)

        # Ensure confirmation was submitted
        if not confirmation:
            return apology("must provide password confirmation", 400)

        # Ensure the confirmation matches the password
        if not check_password_hash(password, confirmation):
            return apology("confirmation does not match password")

        # check to see if username already exists in DB
        if len(db.execute("SELECT username FROM users WHERE username = ?", request.form.get("username"))) != 0:
            return apology("username already exists", 400)

        # Insert into the DB
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                   username, password)
        return redirect("/")

    else:
        return render_template("register.html")


@ app.route("/sell", methods=["GET", "POST"])
@ login_required
def sell():
    """Sell shares of stock"""

    # Query information for the user
    transactions = db.execute("SELECT symbol AS symbol, name AS name, SUM(shares) AS shares, price, SUM(shares * price) AS stock_total FROM transactions WHERE user_id = ? GROUP BY symbol",
                              session["user_id"])

    if request.method == "POST":

        # Ensure stock was selected
        stock = request.form.get("symbol")
        if not stock:
            return apology("no stock was selected", 400)

        # Ensure shares was submitted
        shares = request.form.get("shares")
        if not shares:
            return apology("must provide amount of shares", 400)

        # Ensure whole shares are submitted
        if not shares.isdigit():
            return apology("must provide whole number of shares", 400)

        # Ensure positive amount of shares was submitted
        if int(shares) <= 0:
            return apology("must provide a positive amount of shares", 400)

        # Ensure user has the amount of shares
        stock_number = db.execute("SELECT SUM(shares) AS shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol",
                                  session["user_id"], stock)
        stock_number_int = int(stock_number[0]["shares"])
        if stock_number_int < int(shares):
            return apology("not enough shares", 400)

        # Process everything in the transactions DB
        current_price = lookup(stock)["price"]
        name = lookup(stock)["name"]
        db.execute("INSERT INTO transactions (symbol, name, shares, price, user_id) VALUES (?, ?, ?, ?, ?)",
                   stock, name, -int(shares), current_price, session["user_id"])

        # Update cash field in users database
        cash = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash_after = cash[0]["cash"] + (current_price * int(shares))
        db.execute("UPDATE users SET cash = ? WHERE id = ?",
                   cash_after, session["user_id"])

        return redirect("/")

    else:
        return render_template("sell.html", transactions=transactions, symbol=None)

    # TODO: implement the functionL url_for()
    # TODO: Style the sell.html
    # TODO: change autofocus to dropdown menu when going to sell.html from main menu
