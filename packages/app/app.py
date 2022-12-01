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

# Define jobs
def fetch_yelp_data():
    ''' Job will go here '''
    # Contact API
    API_KEY = os.getenv('API_KEY')
    headers = {'Authorization': 'Bearer {0}'.format(API_KEY)}
    url = 'https://api.yelp.com/v3/businesses/search'
    # Hardcoding state for testing purposes - need to dynamically pass in all states
    params = {'term': 'donut', 'location': 'WA', 'limit': 50, 'offset':0}
        
    # Get request response. Set timeout to stop requests from waiting after 5 seconds
    response = requests.get(url, params=params, headers=headers, timeout=5)

    if response.status_code == 200:
        data = json.loads(response.text)
        print('status code {}'.format(response.status_code))

        # Parse data
        shops = data['businesses']
        for shop in shops:
            name = shop['name'] 
            website = shop['url'] 
            rating = shop['rating'] 
            address = shop['location']['address1'] 
            address2 = shop['location']['address2'] 
            city = shop['location']['city'] 
            state = shop['location']['state'] 
            zip_code = shop['location']['zip_code'] 
            phone = shop['display_phone']
            print(name, rating, address, city)

def my_listener(event):
    if event.exception:
        print('The job crashed :(')
    else:
        print('The job worked :)')

scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(fetch_yelp_data, 'interval', seconds=30)
scheduler.start()
scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

#logging.basicConfig()
#logging.getLogger('apscheduler').setLevel(logging.DEBUG)

# Configure application
app = Flask(__name__)

# Having trouble running flask app and python script for apscheduler at the same time - appears to be working but this conditional still returns false
if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
    

# TODO Need to handle missed job executions, errors that happen w/scheduled jobs

# TODO Error handling print status code
# if response.status_code >= 500:
#     print('[!] [{0}] Server Error: Something is wrong with Yelp'.format(response.status_code))
    #return None
# elif response.status_code == 404:
#     print('[!] [{0}] URL not found: [{1}]'.format(response.status_code,api_url))
    #return None  
# elif response.status_code == 401:
#     print('[!] [{0}] Authentication Failed'.format(response.status_code))
    #return None
# elif response.status_code == 400:
#     print('[!] [{0}] Bad Request'.format(response.status_code))
    #return None
# elif response.status_code >= 300:
#     print('[!] [{0}] Unexpected Redirect'.format(response.status_code))
    #return None
# elif response.status_code == 200:
#     data = json.loads(response.text)
    #pprint(data)
    # print('status code {}'.format(response.status_code))
    # print(response.url)
    #return
# else:
#     print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content))
    #return None

# TODO After sub job of getting data from Yelp api complete, connect to db. Check if records exist, if not create new records. If so, replace/update existing records

# Connect to db
def db_connect():
    connection = sql.connect("donut_shops.db")
    connection.row_factory = sql.Row
    return connection

# Displays all db entries on index.html
# Conditionally renders donut shops by city & state on search.html
@app.route("/", methods=['GET'])
def index():
    states = [('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'),
        ('DE', 'Delaware'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'),
        ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), 
        ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), 
        ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), 
        ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN','Tennessee'), ('TX', 'Texas'), 
        ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')
    ]

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
            return render_template("apology.html", message="No Matches - Please Try Again,", states=states, code=403, selected_city=city, selected_state=state)
        return render_template("index.html", shops=shops, table_title=table_title, states=states, selected_city=city, selected_state=state)

    # Case: city and state are undefined, first time visit to page.
    else:
        table_title = "All Donut Shops"
        shops = cursor.execute("SELECT * FROM shops").fetchall()
        connection.close()
        return render_template("index.html", shops=shops, table_title=table_title, states=states)