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
('hub-c10', '7-in-1 USB-C hub with HDMI', 45.00, 150),
('headphones-b50', 'Noise-cancelling bluetooth headphones', 250.00, 80),
('webcam-1080p', 'Full HD webcam with built-in microphone', 79.99, 120),
('mic-usb-pro', 'Professional USB condenser microphone', 149.00, 60),
('stand-laptop', 'Adjustable aluminum laptop stand', 35.00, 150),
('cable-hdmi-2m', 'Premium 2-meter HDMI 2.1 cable', 19.99, 300),
('charger-65w', 'Compact 65W GaN fast charger', 45.00, 200),
('powerbank-20k', '20000mAh high-capacity power bank', 59.00, 100),
('drive-ssd-1tb', 'Rugged 1TB Portable SSD', 129.00, 90),
('drive-hdd-4tb', '4TB External Hard Drive for backups', 110.00, 85),
('router-ax3000', 'Dual-band Wi-Fi 6 Router', 180.00, 40),
('tablet-pro-11', '11-inch Professional Tablet with 128GB storage', 799.00, 45),
('stylus-pen-2', 'Active Stylus Pen for tablets', 89.00, 110),
('case-tablet-11', 'Protective folio case for 11-inch tablet', 29.00, 150),
('speaker-bt-mini', 'Portable mini Bluetooth speaker', 39.99, 180),
('watch-smart-5', 'Smartwatch with heart rate and fitness tracking', 249.00, 70),
('tracker-gps-mini', 'Compact GPS Tracker for luggage and keys', 29.99, 250),
('dock-thunderbolt', 'Thunderbolt 4 Docking Station with 85W charging', 299.00, 30),
('light-ring-10', '10-inch LED Ring Light with tripod', 49.00, 95),
('screen-green-pop', 'Pop-up Green Screen for streaming', 65.00, 55),
('chair-ergo-mesh', 'Ergonomic Mesh Office Chair with lumbar support', 350.00, 25);

-- Create the audit_log table
CREATE TABLE IF NOT EXISTS audit_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    action VARCHAR(255) NOT NULL,
    details TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);