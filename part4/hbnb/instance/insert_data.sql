-- ADMIN USER
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$e6XSzDPPXfs50H0G5zredOfsjLZuv52dv4nHxjF4JNQdj6.2UXSKe',
    TRUE
);

-- AMENITIES
INSERT INTO amenities (id, name) VALUES
('ff75ecfc-0b82-4ecf-b01e-0637c1c0914c', 'WiFi'),
('91721587-7768-452e-a28c-2ee51879b2fc', 'Swimming Pool'),
('e7efd01a-85c5-49fd-818a-16b6eb0a9570', 'Air Conditioning');