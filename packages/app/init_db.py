import sqlite3 as sql
import json

# clean up step to drop the table

connection = sql.connect('donut_shops.db')
    
with open('schema.sql') as s:
    connection.executescript(s.read())

cursor = connection.cursor()

# drop the db
# cursor.execute("DROP DATABASE donut_shops")
    
with open('response.json') as f:
    data = json.load(f)

    shops = data['businesses']
    
    for shop in shops:
        cursor.execute("INSERT INTO shops (name, website, rating, address, address2, city, state, zip_code, phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (shop["name"], shop["url"], shop["rating"], shop["location"]["address1"], shop["location"]["address2"], shop["location"]["city"], shop["location"]["state"], shop["location"]["zip_code"], shop["display_phone"]))
    
        connection.commit()