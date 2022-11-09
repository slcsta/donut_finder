import sqlite3 as sql
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

connection = sql.connect("dounut_shops.db")

cursor = connection.cursor()

# cursor.execute('CREATE TABLE donut_shops (id INTEGER PRIMARY KEY, name TEXT, address1 TEXT, city TEXT, zip_code TEXT, state TEXT, display_address TEXT, display_phone TEXT, url TEXT)')

connection.close()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        city = request.form.get("city")
        state = state.form.get("state")
        return redirect("/")

    else:
        return render_template("index.html")
