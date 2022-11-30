from flask import Flask, render_template, request, redirect, url_for
import sqlite3 as sql
import requests, json, os, time
from dotenv import load_dotenv
from datetime import datetime
from pprint import pprint
from apscheduler.schedulers.background import BackgroundScheduler

load_dotenv()

# Configure application
app = Flask(__name__)

# Start scheduler 
if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_task, 'interval', seconds=10)
    scheduler.start()

# Define jobs
def scheduled_task():
    ''' Job will go here '''
    print("This task is up and running")

# Need some trigger to keep scheduler on task until stopped

# Contact API
API_KEY = os.getenv('API_KEY')
headers = {'Authorization': 'Bearer {0}'.format(API_KEY)}
url = 'https://api.yelp.com/v3/businesses/search'
# City and state are not assigned value here - need to pass in states
#params = {'term': 'donut', 'location': '{}, {}'.format(str(city), str(state))}
params = {'term': 'donut', 'location': 'New York, NY', 'limit': 50}
        
# Get request response. Set timeout to stop requests frm waiting after 5 seconds
response = requests.get(url, params=params, headers=headers, timeout=5)

# Check status code
pprint(response.url)
print("status code {}".format(response.status_code))

# Print response
data = json.loads(response.text)
pprint(data)

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

    # Calling scheduled task as test
    scheduled_task()
    
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