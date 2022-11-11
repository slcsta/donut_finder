from flask import Flask, render_template, request, redirect
import sqlite3 as sql

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

# Displays all db entries on searched.html matching city & state inputs
# Submit user's input via POST to /search
@app.route("/search", methods=["GET", "POST"])
def search():
    # TODO Lookup func that searches donut shops by city & state
        def lookup(shop):
            # Search value should equal form's inputted city
            # Second search value should contian a state selection from the dropdown menu
            # Est. connection to db then query for shops where city and state match form inputs
            search = db.execute(SELECT * FROM shops WHERE city=request.form.get("city") AND state=request.form.get("state"))
        # If city textbox input value is empty or if city matches none of the citys in db,
        # Then return an error stating "please enter a valid city"
        # Else return rendered searched template with lookup city & state values passed in
    # When form submitted via POST
    if request.method == "POST":
        city = request.form.get("city")
        state = request.form.get("state")

    return render_template("searched.html", search=search)

        

