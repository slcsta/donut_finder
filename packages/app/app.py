from flask import Flask, render_template, request, redirect, url_for
import sqlite3 as sql
from sqlite3 import Error
from .forms import SearchForm

# Configure application
app = Flask(__name__)

# TODO Create a connect to db function here
def db_connect():
    connection = sql.connect("donut_shops.db")
    connection.row_factory = sql.Row
    return connection

# Displays all db entries on index.html
# GET request handling the db query for all donut shops
@app.route("/", methods=["GET", "POST"])
def index():

    search = SearchForm(request.form)
    if request.method == "POST":
        return search_results(search)

    
    else:
        connection = db_connect()
        cursor = connection.cursor()
        shops = cursor.execute("SELECT * FROM shops").fetchall()
        connection.close()
        return render_template("index.html", shops=shops)



# Displays all db entries on searched.html matching city & state inputs
# Submit user's input via POST to /search
@app.route("/search")
def search():
    form = IndexForm()
    if form.validate_on_submit():
        connection = db_connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM shops WHERE city=? AND state=?", (request.form.get("city"), request.form.get("state")))
        search = cursor.fetchall()
        connection.close()
        if search == None:
            print("Please enter a valid city")
        
        return render_template("searched.html", search=search)
        return redirect(url_for("success"))
    return render_template(
        "searched.html",
        form=form,
        template="form-demplate"
    )
    #if request.method == "POST":

        #if not request.form.get("city"):
            #print("Please enter a valid city")

        

        

