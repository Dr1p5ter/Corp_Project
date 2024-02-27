DROP DATABASE IF EXISTS transactions;
CREATE DATABASE IF NOT EXISTS transactions;
USE transactions;

-- GENERATE TABLES --

CREATE TABLE IF NOT EXISTS store_transactions (
    t_id INT NOT NULL AUTO_INCREMENT UNIQUE,
    user_id INT,
    game_id INT,
    date_processed DATETIME NOT NULL,
    refund_availability_before DATETIME NOT NULL,
    PRIMARY KEY (t_id),
    FOREIGN KEY (user_id)
        REFERENCES user_info.login_credentials (user_id),
    FOREIGN KEY (game_id)
        REFERENCES game_connections.game_info (game_id)
);

USE sys;