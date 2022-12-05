from flask import Flask, render_template, request, redirect, url_for
import sqlite3 as sql
import requests, json, os, time, logging
from time import sleep
from dotenv import load_dotenv
from datetime import datetime
from pprint import pprint
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from apscheduler.schedulers.background import BackgroundScheduler

load_dotenv()

logging.basicConfig()

#scheduler = BackgroundScheduler(daemon=True)

STATES = [('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'),
    ('DE', 'Delaware'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'),
    ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), 
    ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), 
    ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), 
    ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN','Tennessee'), ('TX', 'Texas'), 
    ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')]

# Connect to db
def db_connect():
    connection = sql.connect("donut_shops.db")
    connection.row_factory = sql.Row
    return connection

# Detect errors
def detect_error():
    # TODO Handle errors - possibly update function to: https://github.com/Yelp/yelp-python/blob/master/yelp/errors.py
    # Message + status code and that's all I need
    if response.status_code:
        print('Error!'.format(response.status_code))
    # elif response.status_code == 404:
    #     print('[!] [{0}] URL Not Found'.format(response.status_code,api_url))  
    # elif response.status_code == 401:
    #     print('[!] [{0}] Authentication Failed'.format(response.status_code))
    # elif response.status_code == 400:
    #     print('[!] [{0}] Bad Request'.format(response.status_code))
    elif response.status_code == 200:
        data = json.loads(response.text)

def my_listener(event):
    if event.exception:
        logging.warning('The job crashed :(')     
    else:
        logging.info('The job worked :)')

# Define job to fetch Yelp data
def fetch_yelp_data(state):
    API_KEY = os.getenv('API_KEY')
    headers = {'Authorization': 'Bearer {}'.format(API_KEY)}
    url = 'https://api.yelp.com/v3/businesses/search'
    # Data request for each state
    # for state in STATES:
    # Pagination
    donut_shops = []
    #offset = 0
    #while offset <= 50:
    params = {'term': 'donut', 'location': state[0], 'limit': 20, 'offset': 0}
    # Get request response. Set timeout to stop requests from waiting after 5 seconds
    response = requests.get(url, params=params, headers=headers, timeout=5)
    businesses = json.loads(response.text)['businesses']
        # Append results to the donut_shops array
    for business in businesses:
        donut_shops.append(business)
                
    #offset += limit
    print(donut_shops)
        
        # Upsert shops for each state to db        
        # connection = db_connect()
        # cursor = connection.cursor()
        # for shop in donut_shops:
        #     cursor.execute("INSERT INTO shops (name, website, rating, address, address2, city, state, zip_code, phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT (id) DO NOTHING",
        #     (shop["name"], shop["url"], shop["rating"], shop["location"]["address1"], shop["location"]["address2"], shop["location"]["city"], shop["location"]["state"], shop["location"]["zip_code"], shop["display_phone"]))
        #     connection.commit()
        #     print("{state} successfully upserted")
            #connection.close()

scheduler = BackgroundScheduler(daemon=True)
# Add each state as individual job
for state in STATES:
    scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler.add_job(fetch_yelp_data, 'interval', args=[state], max_instances=1, seconds=30)
if not scheduler.running:
    scheduler.start()
    

# scheduler = BackgroundScheduler(daemon=True)
# # possible add each state as individual job
# for state in STATES:
#     scheduler.add_job(fetch_yelp_data, 'interval', seconds=10)
#     scheduler.start()
#     scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
#     print(state)

# Multi row, single column state tracker - get through all pages then reset offset
# Scenario - encounter error - keep goin w/jobs - mark offset in db


#logging.getLogger('apscheduler').setLevel(logging.DEBUG)

# Configure application
app = Flask(__name__)

# This still returns false 
if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0', use_reloader=False)
    
# Displays all db entries on index.html & renders donut shops by city & state on search.html
@app.route("/", methods=['GET'])
def index():
    connection = db_connect()
    cursor = connection.cursor()
    city = request.args.get('city')
    state = request.args.get('state')
    
    # Case: city and state are provided by user and available to use.
    if city and state:
        cursor.execute("SELECT * FROM shops WHERE city=? COLLATE NOCASE AND state=? COLLATE NOCASE", (city, state))
        table_title = "Donut Shop Search Results"
        shops = cursor.fetchall()
        connection.close()
        
        if len(shops) == 0:
            return render_template("apology.html", message="No Matches - Please Try Again,", states=STATES, code=403, selected_city=city, selected_state=state)
        return render_template("index.html", shops=shops, table_title=table_title, states=STATES, selected_city=city, selected_state=state)

    # Case: city and state are undefined, first time visit to page.
    else:
        table_title = "All Donut Shops"
        shops = cursor.execute("SELECT * FROM shops").fetchall()
        connection.close()
        return render_template("index.html", shops=shops, table_title=table_title, states=STATES)