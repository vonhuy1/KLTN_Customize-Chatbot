CREATE DATABASE IF NOT EXISTS pychatbot;
USE pychatbot;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    access_token LONGTEXT NULL,
    refresh_token LONGTEXT NULL,
    expires_at DATETIME NULL
);

CREATE TABLE IF NOT EXISTS chat_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    name_chat VARCHAR(255) ,
    FOREIGN KEY (email) REFERENCES users (email)
);

CREATE TABLE IF NOT EXISTS detail_chat (
    id INT AUTO_INCREMENT PRIMARY KEY,
    chat_id INT,
    YouMessage LONGTEXT NULL,
    AiMessage LONGTEXT NULL,
    data_relevant LONGTEXT NULL,
    source_file LONGTEXT NULL,
    FOREIGN KEY (chat_id) REFERENCES chat_history (id)
);

CREATE TABLE IF NOT EXISTS user_login (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_email VARCHAR(100) NOT NULL,
    user_session_id VARCHAR(100) NOT NULL,
    FOREIGN KEY (user_email) REFERENCES users (email)
);

CREATE TABLE IF NOT EXISTS user_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    uid LONGTEXT,
    email VARCHAR(255) UNIQUE NOT NULL,
    display_name LONGTEXT,
    photo_url LONGTEXT,
    FOREIGN KEY (email) REFERENCES users (email) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS otp (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    otp VARCHAR(6) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
