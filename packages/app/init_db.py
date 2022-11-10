import sqlite3 as sql
import json

with open('response.json') as f:
    data = json.load(f)

# clean up step to drop the table

with sql.connect("donut_shops.db") as connection:
    cursor = connection.cursor()

    with open('schema.sql') as s:
        connection.executescript(s.read())

    with open('response.json') as f:
        shops = json.load(f))

    for shop in shops:
        for location in shop["location"]:
            cursor.execute("INSERT INTO shops (name, website, rating, phone) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (shop["name"], shop["url"], shop["rating"], shop["location"]["city"], shop["location"]["state"], shop["location"]["display_address"], shop["display_phone"]))
        
    connection.commit()