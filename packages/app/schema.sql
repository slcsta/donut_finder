DROP TABLE IF EXISTS shops;

CREATE TABLE shops (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT, 
    website TEXT,
    rating REAL, 
    city TEXT,  
    state TEXT, 
    address TEXT, 
    phone TEXT, 
    url TEXT
)

