from flask import Flask, render_template, request, redirect, url_for
import sqlite3 as sql
import requests, json, os, time, logging
from random import randint
from time import sleep
from dotenv import load_dotenv
from datetime import datetime
from pprint import pprint
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from apscheduler.schedulers.background import BackgroundScheduler

load_dotenv()

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

scheduler = BackgroundScheduler(daemon=True)

STATES = [('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'),
    ('DE', 'Delaware'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'),
    ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), 
    ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), 
    ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), 
    ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN','Tennessee'), ('TX', 'Texas'), 
    ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')]

# Connects to db
def db_connect():
    connection = sql.connect("donut_shops.db")
    connection.row_factory = sql.Row
    return connection

# Detects and logs events
def my_listener(event):
    if event.exception:
        logging.warning('The job crashed :(')     
    else:
        logging.info('The job worked :)')

# Defines job to fetch Yelp data
def fetch_yelp_data(state):
    API_KEY = os.getenv('API_KEY')
    headers = {'Authorization': 'Bearer {}'.format(API_KEY)}
    url = 'https://api.yelp.com/v3/businesses/search'
    
    # Paginates results using offset and limit 
    limit = 20
    offset = 0
    while offset <= 40:
        params = {'term': 'donut', 'location': state[0], 'limit': limit, 'offset': offset}
        response = requests.get(url, params=params, headers=headers, timeout=15)
        print(response)
        donut_shops = response.json()['businesses']
        print(donut_shops)
        # Upserts donut shops 
        # Batch insert these - Look up sqlite docs on this 
        for shop in donut_shops:
            print(shop["name"])      
        connection = db_connect()
        cursor = connection.cursor()
        for shop in donut_shops:
            cursor.execute("INSERT INTO shops (name, website, rating, address, address2, city, state, zip_code, phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT (address) DO NOTHING",
            (shop["name"], shop["url"], shop["rating"], shop["location"]["address1"], shop["location"]["address2"], shop["location"]["city"], shop["location"]["state"], shop["location"]["zip_code"], shop["display_phone"]))
            connection.commit()
        # could instead pull the offset number from the response
        offset += limit
        sleep(randint(10, 30))
    connection.close()
    

# Schedules jobs
scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
for state in STATES:
    scheduler.add_job(fetch_yelp_data, 'interval', args=[state], seconds=15)
    if not scheduler.running:
        scheduler.start()
    
# Configures Flask app
app = Flask(__name__)

# Enables app and scheduler to run concurrently
if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0', use_reloader=False)

# Displays all db entries & renders donut shops by city & state on index.html
@app.route("/", methods=['GET'])
def index():
    connection = db_connect()
    cursor = connection.cursor()
    city = request.args.get('city')
    state = request.args.get('state')
    
    # Case: city and state are provided by user and available to use.
    if city and state:
        cursor.execute("SELECT * FROM shops WHERE city=? COLLATE NOCASE AND state=? COLLATE NOCASE ORDER BY state, city, name, address, rating", (city, state))
        table_title = "Donut Shop Search Results"
        shops = cursor.fetchall()
        connection.close()
        
        if len(shops) == 0:
            return render_template("apology.html", message="No Matches - Please Try Again,", states=STATES, code=403, selected_city=city, selected_state=state)
        return render_template("index.html", shops=shops, table_title=table_title, states=STATES, selected_city=city, selected_state=state)

    # Case: city and state are undefined, first time visit to page.
    else:
        table_title = "All Donut Shops"
        shops = cursor.execute("SELECT * FROM shops ORDER BY state, city, name, address, rating").fetchall()
        connection.close()
        return render_template("index.html", shops=shops, table_title=table_title, states=STATES)