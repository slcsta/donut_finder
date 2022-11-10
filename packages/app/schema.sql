DROP TABLE IF EXISTS shops;

CREATE TABLE shops (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT, 
    website TEXT,
    rating REAL,
    address TEXT,
    address2 TEXT, 
    city TEXT,  
    state TEXT, 
    zip_code TEXT,
    phone TEXT 
);

