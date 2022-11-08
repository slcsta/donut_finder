import sqlite3 as sql
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

connection = sql.connect("dounut_shops.db")
print "Opened database successfully";

cursor = connection.cursor()

connection.close()

db = '/path/to/database.db'

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        city = request.form.get("city")
        state = state.form.get("state")
        return redirect("/")

    else:
        return render_template("index.html")
