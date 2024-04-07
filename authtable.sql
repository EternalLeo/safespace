CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT, 
    passhash TEXT,
    salt TEXT,
    publickey TEXT,
    privatekey TEXT
);