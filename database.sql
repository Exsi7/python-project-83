DROP TABLE IF EXISTS urls;
DROP TABLE IF EXISTS url_checks;
CREATE TABLE urls (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name varchar(255),
    created_at timestamp
);
CREATE TABLE url_checks (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    url_id bigint,
    status_code integer,
    h1 text,
    title text,
    description text,
    created_at date
);