-- schema.sql — structura bazei de date de audit
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    sam_account_name TEXT PRIMARY KEY,
    name             TEXT NOT NULL,
    department       TEXT NOT NULL,
    enabled          INTEGER NOT NULL,   -- 0/1
    last_logon_days  INTEGER NOT NULL
);
