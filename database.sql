DROP TABLE IF EXISTS urls;
CREATE TABLE urls (
    id serial PRIMARY KEY,
    name varchar(255),
    created_at timestamp
);