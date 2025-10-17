CREATE DATABASE IF NOT EXISTS betty;

USE betty;

CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    INDEX (product_name)
);

INSERT INTO products (product_name, price) VALUES
('Bird Seed Mix', 15.99),
('Sunflower Seeds', 22.50),
('Suet Cakes', 12.75),
('Bird Feeder', 25.00),
('Bluebird House', 35.50),
('Bird Bath', 75.99),
('Cuttlebone', 4.25),
('Millet', 8.00),
('Parrot Pellets', 28.99),
('Finch & Canary Food', 10.50);
