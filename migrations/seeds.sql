DROP TABLE IF EXISTS users;

CREATE TABLE users(
    user_id serial PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(300) NOT NULL,
    games_won NUMERIC
);
