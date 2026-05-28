DROP DATABASE IF EXISTS day4_v1;
CREATE DATABASE day4_v1 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE day4_v1;

CREATE TABLE roles (
    role_id INT PRIMARY KEY AUTO_INCREMENT,
    role_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(100) NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(50) NOT NULL,
    role_id INT NOT NULL,
    FOREIGN KEY (role_id) REFERENCES roles(role_id)
);

CREATE TABLE items (
    item_id INT PRIMARY KEY AUTO_INCREMENT,
    item_name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    image VARCHAR(100),
    category VARCHAR(100) NOT NULL
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    item_id INT NULL,
    item_name VARCHAR(100) NOT NULL,
    quantity INT NOT NULL,
    delivery_type VARCHAR(50) NOT NULL,
    delivery_place VARCHAR(200) NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'Новый',
    order_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES items(item_id) ON DELETE SET NULL
);

CREATE TABLE discounts (
    discount_id INT PRIMARY KEY AUTO_INCREMENT,
    item_id INT NOT NULL,
    discount_percent INT NOT NULL,
    date_start DATE NOT NULL,
    date_end DATE NOT NULL,
    FOREIGN KEY (item_id) REFERENCES items(item_id) ON DELETE CASCADE
);
