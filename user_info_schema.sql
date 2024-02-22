DROP DATABASE IF EXISTS user_info;
CREATE DATABASE IF NOT EXISTS user_info;
USE user_info;

-- GENERATE TABLES --

CREATE TABLE IF NOT EXISTS login_credentials (
    user_id INT NOT NULL AUTO_INCREMENT UNIQUE,
    login_username VARCHAR(16) NOT NULL,
    login_password VARCHAR(32) NOT NULL,
    last_password_change DATETIME,
    need_password_change DATETIME,
    PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS profile_info (
    user_id INT NOT NULL,
    fname VARCHAR(32),
    minit VARCHAR(1),
    lname VARCHAR(32),
    b_date DATE,
    age INT,
    date_registered DATETIME,
    FOREIGN KEY (user_id)
        REFERENCES login_credentials (user_id),
    CONSTRAINT CHK_profile_info CHECK (age >= 0)
);

CREATE TABLE IF NOT EXISTS permissions (
    user_id INT NOT NULL,
    strike_count INT NOT NULL,
    text_coms_public BOOL,
    text_coms_friend BOOL,
    voice_coms_public BOOL,
    voice_coms_friend BOOL,
    last_strike_made DATETIME,
    date_to_clean_strikes DATETIME,
    FOREIGN KEY (user_id)
        REFERENCES login_credentials (user_id),
    CONSTRAINT CHK_strike_count CHECK (0 <= strike_count AND strike_count <= 3)
);

CREATE TABLE IF NOT EXISTS follows_user (
    user1_id INT NOT NULL,
    user2_id INT NOT NULL,
    followed_since DATETIME NOT NULL,
    FOREIGN KEY (user1_id)
        REFERENCES login_credentials (user_id),
    FOREIGN KEY (user2_id)
        REFERENCES login_credentials (user_id)
);

USE sys;