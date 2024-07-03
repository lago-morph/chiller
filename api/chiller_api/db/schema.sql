CREATE TABLE users 
( 
    id      serial primary key, 
    name    TEXT UNIQUE NOT NULL
);

CREATE TABLE movielist (
    id      serial primary key,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
