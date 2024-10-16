

CREATE DATABASE IF NOT EXISTS game_db;
USE game_db;
CREATE TABLE IF NOT EXISTS user(
id int NOT NULL AUTO_INCREMENT,
username varchar(50) NOT NULL UNIQUE,
password varchar(255) NOT NULL,
email varchar(100) NOT NULL,
score INT DEFAULT 0,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
PRIMARY KEY (id)
);

select * from user;
CREATE TABLE IF NOT EXISTS teacher(
id int NOT NULL AUTO_INCREMENT,
username varchar(50) NOT NULL UNIQUE,
password varchar(255) NOT NULL,
email varchar(100) NOT NULL,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY (id)
);

Select * from user


















