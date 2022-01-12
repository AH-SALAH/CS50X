import os

# from cs50 import SQL
import sqlite3
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from helpers import toDict

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
# db = SQL("sqlite:///birthdays.db")
DBURL = 'birthdays.db'


@app.route("/", methods=["GET", "POST"])
def index():
    # open db here to solve same thread prob
    # https://stackoverflow.com/questions/48218065/programmingerror-sqlite-objects-created-in-a-thread-can-only-be-used-in-that-sa
    with sqlite3.connect(DBURL) as db:
        cursor = db.cursor()
        resp = ""
        if request.method == "POST":
            # Add the user's entry into the database
            name = request.form.get('name')
            month = request.form.get('month', type=int)
            day = request.form.get('day', type=int)

            cursor.execute("INSERT INTO birthdays (name, month, day) VALUES(?, ?, ?)",
                           (name, month, day))
            resp = redirect("/")

        else:

            # Display the entries in the database on index.html
            data = cursor.execute("SELECT * FROM birthdays")
            # change data tuple to list of dict
            # cursor.row_factory = lambda C, R: { c[0]: R[i] for i, c in enumerate(C.description) }
            rows = toDict(data)

            resp = render_template("index.html", rows=rows)

        return resp


@app.route('/edit/<int:id>', methods=["GET", "POST"])
def edit(id):
    if not id:
        return redirect('/')

    if request.method == "POST":
        with sqlite3.connect(DBURL) as db:
            name = request.form.get('name')
            month = request.form.get('month', type=int)
            day = request.form.get('day', type=int)

            cursor = db.cursor()
            data = cursor.execute(
                "UPDATE birthdays SET name = ?, month = ?, day = ? WHERE id = ?", (name, month, day, id))
            print("data: ", data)
            return redirect('/')
    else:
        with sqlite3.connect(DBURL) as db:

            cursor = db.cursor()
            data = cursor.execute(
                "SELECT * FROM birthdays WHERE id = ?", (id,))
            return render_template('edit.html', row=toDict(data)[0])


@app.route('/delete/<int:id>')
def delete(id):
    if not id:
        return redirect('/')

    with sqlite3.connect(DBURL) as db:
        cursor = db.cursor()
        cursor.execute(
            "DELETE FROM birthdays WHERE id = ?", (id,))
        return redirect('/')
