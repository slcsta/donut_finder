import sqlite3 as sql
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def get_db_connection():
    conn = sql.connect('donut_shops.db')
    conn.row_factory = sql.row_factory
    return conn

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        city = request.form.get("city")
        state = state.form.get("state")
        return redirect("/")

    else:
        birthdays = db.execute("SELECT * FROM shops")
        return render_template("index.html", shops=shops)
