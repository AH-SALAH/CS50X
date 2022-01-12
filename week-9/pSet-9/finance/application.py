import os

from cs50 import SQL
from flask import Flask
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from helpers import apology
from settings import Settings

from routes.routes import Routes

# Configure application
app = Flask(__name__)

settings = Settings(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

# ################################
with app.app_context():
    Routes(app, db, settings)

# ################################
def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    if e.code == 413:
        return "File is too large", 413
    return apology(e.name, e.code)

# ################################
# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
