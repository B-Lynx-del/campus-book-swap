CREATE DATABASE book_swap;
USE book_swap;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(255),  -- Hash in production!
    email VARCHAR(100)
);
CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    author VARCHAR(100),
    description TEXT,
    price DECIMAL(10,2),
    condition VARCHAR(50),
    type ENUM('sell', 'trade', 'buy'),
    owner_id INT,
    FOREIGN KEY (owner_id) REFERENCES users(id)
);
CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT,
    receiver_id INT,
    book_id INT,
    message TEXT,
    FOREIGN KEY (sender_id) REFERENCES users(id),
    FOREIGN KEY (receiver_id) REFERENCES users(id),
    FOREIGN KEY (book_id) REFERENCES books(id)
);