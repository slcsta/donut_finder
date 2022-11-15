from flask import Flask, render_template, request, redirect, url_for
import sqlite3 as sql
from sqlite3 import Error
from forms import SearchForm
# from flask_wtf.csrf import CSRFProtect

# Configure application
app = Flask(__name__)


# Connect to db function here
def db_connect():
    connection = sql.connect("donut_shops.db")
    connection.row_factory = sql.Row
    return connection

# Displays all db entries on index.html
# GET request handling the db query for all donut shops
# Conditionally render db query for donut shops by city & state
@app.route("/", methods=['GET'])
def index():
    connection = db_connect()
    cursor = connection.cursor()
    city = request.args.get('city')
    state = request.args.get('state')
    
    if city and state:
        cursor.execute("SELECT * FROM shops WHERE city=? AND state=?", (request.args.get("city"), request.args.get("state")))
        results = cursor.fetchall()
        return render_template("search.html", results=results)

    else:
        shops = cursor.execute("SELECT * FROM shops").fetchall()
        connection.close()
        return render_template("index.html", shops=shops)