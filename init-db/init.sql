CREATE TABLE addresses(
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    place VARCHAR(100) NOT NULL,
    district VARCHAR(100) NOT NULL
);

CREATE TABLE geolocation(
    id SERIAL PRIMARY KEY,
    address_id INT UNIQUE REFERENCES addresses(id),
    latitude DECIMAL,
    longitude DECIMAL
);