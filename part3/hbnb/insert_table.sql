-- ADMIN USER
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$KIX8QFvD2f8lE9v6R3JQ6eKf7xqU1F6hQ2j1rZQ7w7xBz8Q7iX6dO',
    TRUE
);

-- AMENITIES
INSERT INTO amenities (id, name) VALUES
('b1e2b4a0-8e4a-4e3a-9c2e-2b3a4e5a6b7c', 'WiFi'),
('c2f3c5b1-9f5b-4d4b-8d3f-3c4b5f6c7d8e', 'Swimming Pool'),
('d3a4d6c2-af6c-5e5c-9e4a-4d5c6e7f8a9b', 'Air Conditioning');