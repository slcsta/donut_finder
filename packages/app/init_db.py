import sqlite3 as sql
import json

with open('response.json') as f:
    data = json.load(f)

connection = sql.connect("dounut_shops.db")

with open('schema.sql') as s:
    connection.executescript(s.read())

cursor = connection.cursor()

with open('response.json') as f:
    data = json.load(f)

businesses = data["businesses"]

for business in businesses:
    cursor.execute("INSERT INTO shops (name, website, rating, phone) VALUES (?, ?, ?, ?)",
    (business["name"], business["url"], business["rating"], business["display_phone"]))

connection.close()