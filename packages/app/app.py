import sqlite3 as sql
from flask import Flask, render_template, request, redirect

# Configure application
app = Flask(__name__)

# TODO Create a connect to db function here


# Displays all db entries on index.html
# GET request handling the db query for all donut shops
@app.route("/")
def index():
    connection = sql.connect("donut_shops.db")
    connection.row_factory = sql.Row
    cursor = connection.cursor()
    shops = cursor.execute("SELECT * FROM shops")
    return render_template("index.html", shops=shops)

@app.route("/shop", methods=["GET", "POST"])
def shop():
    # When form is submitted via Post
    # TODO Call a lookup func that searches donut shops by city & state 
    # TODO Require that a user enter a city and select state from dropdown
    if request.method == "POST":
    #   city = request.form.get("city")
    #   state = request.form.get("state")
    

        
