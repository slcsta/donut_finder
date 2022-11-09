DROP TABLE IF EXISTS shops;

CREATE TABLE shops (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT, 
    address1 TEXT, 
    city TEXT, 
    zip_code TEXT, 
    state TEXT, 
    display_address TEXT, 
    display_phone TEXT, 
    url TEXT
)

