DROP DATABASE IF EXISTS transactions;
CREATE DATABASE IF NOT EXISTS transactions;
USE transactions;

-- GENERATE TABLES --

CREATE TABLE IF NOT EXISTS store_transactions (
    t_id INT NOT NULL AUTO_INCREMENT UNIQUE,
    user_id INT,
    game_id INT,
    PRIMARY KEY (t_id),
    FOREIGN KEY (user_id)
        REFERENCES user_info.login_credentials (user_id),
	FOREIGN KEY (game_id)
		REFERENCES game_connections.game_info (game_id)
);

CREATE TABLE IF NOT EXISTS transaction_count_per_user (
    user_id INT NOT NULL,
    num_of_purchases INT,
    FOREIGN KEY (user_id)
        REFERENCES user_info.login_credentials (user_id)
);

USE sys;