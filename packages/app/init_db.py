import sqlite3 as sql

connection = sql.connect("dounut_shops.db")

with open('schema.sql') as f:
    connection.executescript(f.read())

name =

cursor = connection.cursor()

connection.close()