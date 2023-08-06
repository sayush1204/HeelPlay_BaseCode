ALTER USER 'root'@'localhost' IDENTIFIED BY 'heelplay';
CREATE DATABASE heel_play_db;
USE heel_play_db;

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL,
  password VARCHAR(100) NOT NULL,
  hashed_password VARCHAR(100) NOT NULL;
  graduation_year INT,
  major VARCHAR(255),
  sport VARCHAR(255),
  position VARCHAR(255),
  bio TEXT,
  profile_pic VARCHAR(255)
);
