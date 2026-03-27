
-- SQL statements to seed market data for testing
-- Example: INSERT INTO assets (name, price) VALUES ('Gold', 1800.00);
-- Example: INSERT INTO users (username, password_hash) VALUES ('testuser', 'hashed_password');
-- PILLAR: DATA INTEGRITY - Schema Definition
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    sku VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100),
    price DECIMAL(18, 2)
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    order_status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Seed Data for Nuam Simulation
INSERT INTO products (sku, name, price) 
VALUES ('ECOPETROL.CB', 'Ecopetrol SA', 2450.00)
ON CONFLICT (sku) DO NOTHING;
