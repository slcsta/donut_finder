import sqlite3 as sql
import json
from flatten_json import flatten

with open('response.json') as f:
    data = json.load(f)

# clean up step to drop the table

with sql.connect("donut_shops.db") as connection:
    cursor = connection.cursor()

    with open('schema.sql') as s:
        connection.executescript(s.read())

    with open('response.json') as f:
        data = json.load(f)

    shops = data["businesses"]
    flatten(shops)
    for shop in shops:
        cursor.execute("INSERT INTO shops (name, website, rating, phone) VALUES (?, ?, ?, ?)",
        (shop["name"], shop["url"], shop["rating"], shop["location"]["city"], shop["location"]["state"], shop["location"]["display_address"], shop["display_phone"]))
        
    connection.commit()