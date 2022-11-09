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
        data = json.load(f)

    businesses = data["businesses"]

    for business in businesses:
        cursor.execute("INSERT INTO shops (name, website, rating, phone) VALUES (?, ?, ?, ?)",
        (business["name"], business["url"], business["rating"], business["display_phone"]))
        
    connection.commit()