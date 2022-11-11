from flask import Flask, render_template, request, redirect
import sqlite3 as sql
from sqlite3 import Error

# Configure application
app = Flask(__name__)

# TODO Create a connect to db function here
def db_connect():
    connection = sql.connect("donut_shops.db")
    connection.row_factory = sql.Row
    return connection

# Displays all db entries on index.html
# GET request handling the db query for all donut shops
@app.route("/")
def index():
    connection = db_connect()
    cursor = connection.cursor()
    shops = cursor.execute("SELECT * FROM shops").fetchall()
    connection.close()
    return render_template("index.html", shops=shops)

# Displays all db entries on searched.html matching city & state inputs
# Submit user's input via POST to /search
@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        connection = db_connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM shops WHERE city=? AND state=?", (request.form.get("city"), request.form.get("state")))
        search = cursor.fetchall()
        connection.close()
        return render_template("searched.html", search=search)

        

