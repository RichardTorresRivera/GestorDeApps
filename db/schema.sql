CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Datos prueba ususarios
INSERT INTO users (name, email) VALUES
('Juan Pérez', 'juan@example.com'),
('Ana Gómez', 'ana@example.com'),
('Carlos Ruiz', 'carlos@example.com');

-- Datos prueba productos
INSERT INTO products (name, description, price) VALUES
('Laptop Lenovo', 'Laptop de 14 pulgadas con 8GB RAM', 750.00),
('Teclado Mecánico', 'Teclado retroiluminado con switches rojos', 120.50),
('Monitor LG 24"', 'Monitor Full HD 1080p', 180.99);
