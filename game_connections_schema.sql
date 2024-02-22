DROP DATABASE IF EXISTS game_connections;
CREATE DATABASE IF NOT EXISTS game_connections;
USE game_connections;

-- GENERATE TABLES --

CREATE TABLE IF NOT EXISTS publisher (
    pub_id INT NOT NULL AUTO_INCREMENT UNIQUE,
    pub_name VARCHAR(32) NOT NULL,
    pub_start_up_date DATE,
    pub_game_count INT NOT NULL,
    PRIMARY KEY (pub_id)
);

CREATE TABLE IF NOT EXISTS game_info (
    game_id INT NOT NULL AUTO_INCREMENT UNIQUE,
    pub_id INT NOT NULL,
    game_name VARCHAR(64) NOT NULL,
    price INT NOT NULL,
    release_date DATE,
    PRIMARY KEY (game_id),
    FOREIGN KEY (pub_id)
        REFERENCES publisher (pub_id)
);

USE sys;