-- DELETE FROM shops
-- WHERE id IN(
--     SELECT id FROM shops
--     EXCEPT SELECT MIN(id) FROM shops
--     GROUP BY address
-- );

SELECT * FROM shops ORDER BY state, city, name, address, rating;
--SELECT * FROM shops ON CONFLICT(address) DO UPDATE SET ignores ORDER BY state, city, name, address, rating;
--PRAGMA foreign_keys=off;

-- BEGIN TRANSACTION;

-- ALTER TABLE shops RENAME TO old_shops;

-- CREATE TABLE shops (   
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     name TEXT,
--     website TEXT,
--     rating REAL,
--     address TEXT,
--     address2 TEXT, 
--     city TEXT,  
--     state TEXT, 
--     zip_code TEXT,
--     phone TEXT, 
--     CONSTRAINT address_unique UNIQUE (address)
-- );

-- INSERT INTO shops SELECT * FROM old_shops;

-- COMMIT;

--PRAGMA foreign_keys=on;