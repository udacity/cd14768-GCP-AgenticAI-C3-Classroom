-- Create the warehouse database
CREATE DATABASE IF NOT EXISTS warehouse;
USE warehouse;

-- Create the products table
CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT NOT NULL
);

-- Insert sample data into products table
INSERT INTO products (name, description, price, stock_quantity) VALUES
('lap-1000', 'High-performance laptop for professionals', 1500.00, 50),
('mouse-42', 'Ergonomic wireless mouse', 25.00, 200),
('kbd-70', 'RGB mechanical keyboard with tactile switches', 120.00, 100),
('mon-4027a', '27-inch 4K UHD monitor', 400.00, 75),
('hub-c10', '7-in-1 USB-C hub with HDMI', 45.00, 150);

-- Create the audit_log table
CREATE TABLE IF NOT EXISTS audit_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    action VARCHAR(255) NOT NULL,
    details TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);