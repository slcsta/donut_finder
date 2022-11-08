import sqlite3 as sql
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

con = sql.connect("dounut_shops.db")

db = '/path/to/database.db'



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        city = request.form.get("city")
        state = state.form.get("state")
        return redirect("/")

    else:
        return render_template("index.html")
