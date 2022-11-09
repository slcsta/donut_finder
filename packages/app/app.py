import sqlite3 as sql
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        city = request.form.get("city")
        state = state.form.get("state")
        return redirect("/")

    else:
        connection = sql.connect("donut_shops.db")
        connection.row_factory = sql.Row
        cursor = connection.cursor()
        shops = cursor.execute("SELECT * FROM shops")
        #rows = cursor.fetchall()
        return render_template("index.html", shops=shops)
