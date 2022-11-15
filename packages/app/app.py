from flask import Flask, render_template, request, redirect, url_for
import sqlite3 as sql
from sqlite3 import Error
from forms import SearchForm
# from flask_wtf.csrf import CSRFProtect

# Configure application
app = Flask(__name__)


# TODO Create a connect to db function here
def db_connect():
    connection = sql.connect("donut_shops.db")
    connection.row_factory = sql.Row
    return connection

# Displays all db entries on index.html
# GET request handling the db query for all donut shops
# '/' takes query params of city and state and then re
#@app.route("/", methods=["GET", "POST"])
@app.route("/", methods=['GET'])
def index():
    #search = SearchForm(request.form)
    #if search:
    connection = db_connect()
    cursor = connection.cursor()
    city = request.args.get('city')
    state = request.args.get('state')
    print(state)
    
    if city and state:
        cursor.execute("SELECT * FROM shops WHERE city=? AND state=?", (request.args.get("city"), request.args.get("state")))
        shops = cursor.fetchall()
        return render_template("search.html", results=results)

    else:
        shops = cursor.execute("SELECT * FROM shops").fetchall()
        connection.close()
        return render_template("index.html", shops=shops)


    # elif not que:
    #     return redirect(url_for('index'))

    # if request.method == "POST":
        # Validate that post form is successfully submitted
        # Return submitted input fields
        # Redirect to "/results" url
        # if search.validate():
        #     print(search)
        #     return search 
    
    # else:
    #     connection = db_connect()
    #     cursor = connection.cursor()
    #     shops = cursor.execute("SELECT * FROM shops").fetchall()
    #     connection.close()
    #     return render_template("index.html", shops=shops, form=search)

# Displays db entries on results.html that match city & state inputs
# @app.route("/results")
# def search_results(search):
#     form = SearchForm()
#     connection = db_connect()
#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM shops WHERE city=? AND state=?", (request.form.get("city"), request.form.get("state")))
#     search = cursor.fetchall()
#     connection.close()
        
#     if search == None:
#         print("Please enter a valid city")

#     return render_template(
#         "results.html",
#         form=form,
#         template="form-template"
#     )
        #if not request.form.get("city"):
            #print("Please enter a valid city")

        

        

