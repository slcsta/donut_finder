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
    shops = connection.execute("SELECT * FROM shops").fetchall()
    connection.close()
    return render_template("index.html", shops=shops)

# Displays all db entries on searched.html matching city & state inputs
# Submit user's input via POST to /search
@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        connection = db_connect()
        cursor = connection.cursor()
        city = request.form.get("city")
        state = request.form.get("state")
    # TODO Lookup func that searches donut shops by city & state
        #def lookup(shop):
            # Search value should equal form's inputted city
            # Second search value should contian a state selection from the dropdown menu
            # Est. connection to db then query for shops where city and state match form inputs
        cursor.execute("SELECT * FROM shops WHERE city=city AND state=state")
        search = cursor.fetchall()
        connection.close()
        # If city textbox input value is empty or if city matches none of the citys in db,
        # Then return an error stating "please enter a valid city"
        # Else return rendered searched template with lookup city & state values passed in
    # When form submitted via POST
        return render_template("searched.html", search=search)

        

