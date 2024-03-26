DROP DATABASE IF EXISTS transactions;
DROP DATABASE IF EXISTS game_connections;
DROP DATABASE IF EXISTS user_info;
DROP DATABASE IF EXISTS user_info;
CREATE DATABASE IF NOT EXISTS user_info;
USE user_info;

-- GENERATE TABLES --

CREATE TABLE IF NOT EXISTS login_credentials (
    user_id INT NOT NULL AUTO_INCREMENT UNIQUE,
    login_username VARCHAR(16) NOT NULL UNIQUE,
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
DROP DATABASE IF EXISTS game_connections;
CREATE DATABASE IF NOT EXISTS game_connections;
USE game_connections;

-- GENERATE TABLES --

CREATE TABLE IF NOT EXISTS publisher (
    pub_id INT NOT NULL AUTO_INCREMENT UNIQUE,
    pub_name VARCHAR(32) NOT NULL,
    pub_start_up_date DATE,
    pub_game_count INT NOT NULL DEFAULT 0,
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
-- GENERATE TRIGGERS FOR user_info --

DELIMITER //

USE user_info//

DROP TRIGGER IF EXISTS insert_before_login_credentials//
CREATE TRIGGER insert_before_login_credentials
BEFORE INSERT ON user_info.login_credentials
FOR EACH ROW
BEGIN
	SET NEW.need_password_change = DATE_ADD(NOW(), INTERVAL 6 MONTH);
    SET NEW.last_password_change = NOW();
END;//

DROP TRIGGER IF EXISTS insert_after_login_credentials//
CREATE TRIGGER insert_after_login_credentials
AFTER INSERT ON user_info.login_credentials
FOR EACH ROW
BEGIN
	INSERT INTO profile_info (user_id) VALUES (NEW.user_id);
    INSERT INTO permissions (user_id, strike_count, text_coms_public, text_coms_friend, voice_coms_public, voice_coms_friend, last_strike_made, date_to_clean_strikes) VALUES (NEW.user_id, 0, TRUE, TRUE, TRUE, TRUE, NOW(), NOW());
END;//

DROP TRIGGER IF EXISTS update_login_credentials//
CREATE TRIGGER update_login_credentials
BEFORE UPDATE ON user_info.login_credentials
FOR EACH ROW
BEGIN
	IF NEW.login_password <> OLD.login_password THEN
		SET NEW.need_password_change = DATE_ADD(NOW(), INTERVAL 6 MONTH);
		SET NEW.last_password_change = NOW();
	END IF;
END;//

DROP TRIGGER IF EXISTS delete_login_credentials//
CREATE TRIGGER delete_login_credentials
BEFORE DELETE ON user_info.login_credentials
FOR EACH ROW
BEGIN
	DELETE FROM profile_info
	WHERE profile_info.user_id = OLD.user_id;
    
    DELETE FROM permissions
    WHERE permissions.user_id = OLD.user_id;
    
    DELETE FROM follows_user
    WHERE follows_user.user1_id = OLD.user_id
    OR follows_user.user2_id = OLD.user_id;
    
    UPDATE transactions.store_transactions
    SET transactions.store_transactions.user_id = NULL
    WHERE transactions.store_transactions.user_id = OLD.user_id;
END;//

DROP TRIGGER IF EXISTS insert_profile_info//
CREATE TRIGGER insert_profile_info
BEFORE INSERT ON user_info.profile_info
FOR EACH ROW
BEGIN
	SET NEW.date_registered = NOW();
END;//

DROP TRIGGER IF EXISTS update_profile_info//
CREATE TRIGGER update_profile_info
BEFORE UPDATE ON user_info.profile_info
FOR EACH ROW
BEGIN
	IF NEW.b_date IS NOT NULL THEN
		SET NEW.age = DATE_FORMAT(FROM_DAYS(DATEDIFF(NOW(), NEW.b_date)), '%Y');
	ELSE
		SET NEW.age = NULL;
	END IF;
END;//

DROP TRIGGER IF EXISTS update_permissions//
CREATE TRIGGER update_permissions
BEFORE UPDATE ON user_info.permissions
FOR EACH ROW
BEGIN
	IF NEW.strike_count = 1 THEN
		SET NEW.text_coms_public = FALSE;
        SET NEW.voice_coms_public = FALSE;
        SET NEW.last_strike_made = NOW();
        SET NEW.date_to_clean_strikes = DATE_ADD(NOW(), INTERVAL 5 MINUTE);
	ELSEIF NEW.strike_count = 2 THEN
		SET NEW.text_coms_friend = FALSE;
        SET NEW.voice_coms_friend = FALSE;
        SET NEW.last_strike_made = NOW();
        SET NEW.date_to_clean_strikes = DATE_ADD(NOW(), INTERVAL 30 MINUTE);
	ELSEIF NEW.strike_count > 2 THEN
		SET NEW.last_strike_made = NOW();
        SET NEW.date_to_clean_strikes = DATE_ADD(NOW(), INTERVAL 1 HOUR);
	END IF;
END;//

-- GENERATE TRIGGERS FOR game_connections --

USE game_connections//

DROP TRIGGER IF EXISTS update_publisher_from_game_insert//
CREATE TRIGGER update_publisher_from_game_insert
BEFORE INSERT ON game_connections.game_info
FOR EACH ROW
BEGIN
	DECLARE previous_game_count INT;
    SET previous_game_count = (SELECT pub_game_count FROM game_connections.publisher WHERE pub_id = NEW.pub_id);
	UPDATE game_connections.publisher
    SET pub_game_count = previous_game_count + 1
    WHERE pub_id = NEW.pub_id;
END;//

-- GENERATE TRIGGERS FOR transactions --

USE transactions//

DELIMITER ;

USE sys;
-- GENERATE EVENTS FOR user_info --

DELIMITER //

DROP EVENT IF EXISTS user_info.update_strike_count_event//
CREATE EVENT user_info.update_strike_count_event
ON SCHEDULE EVERY 1 SECOND
DO
	BEGIN
		UPDATE user_info.permissions
		SET strike_count = 0
		WHERE strike_count > 0 AND
        date_to_clean_strikes < NOW();

		CREATE OR REPLACE VIEW strike_time_remaining AS
		SELECT user_id, strike_count, last_strike_made, date_to_clean_strikes, 
		TIMESTAMPDIFF(DAY, NOW(), date_to_clean_strikes) AS days_remaining,
		TIMESTAMPDIFF(HOUR, NOW(), date_to_clean_strikes) - TIMESTAMPDIFF(DAY, NOW(), date_to_clean_strikes) * 24 AS hours_remaining,
		TIMESTAMPDIFF(MINUTE, NOW(),date_to_clean_strikes) - TIMESTAMPDIFF(HOUR, NOW(), date_to_clean_strikes) * 60 AS minites_remaining,
		TIMESTAMPDIFF(SECOND, NOW(),date_to_clean_strikes) - TIMESTAMPDIFF(MINUTE, NOW(), date_to_clean_strikes) * 60 AS seconds_remaining
		FROM user_info.permissions
		WHERE strike_count > 0
		ORDER BY days_remaining ASC, hours_remaining ASC, minites_remaining ASC, seconds_remaining ASC;
	END//

DELIMITER ;
-- GENERATE VIEWS FOR user_info --

CREATE OR REPLACE VIEW strike_time_remaining AS
SELECT user_id, strike_count, last_strike_made, date_to_clean_strikes, 
TIMESTAMPDIFF(DAY, NOW(), date_to_clean_strikes) AS days_remaining,
TIMESTAMPDIFF(HOUR, NOW(), date_to_clean_strikes) - TIMESTAMPDIFF(DAY, NOW(), date_to_clean_strikes) * 24 AS hours_remaining,
TIMESTAMPDIFF(MINUTE, NOW(),date_to_clean_strikes) - TIMESTAMPDIFF(HOUR, NOW(), date_to_clean_strikes) * 60 AS minites_remaining,
TIMESTAMPDIFF(SECOND, NOW(),date_to_clean_strikes) - TIMESTAMPDIFF(MINUTE, NOW(), date_to_clean_strikes) * 60 AS seconds_remaining
FROM user_info.permissions
WHERE strike_count > 0
ORDER BY days_remaining ASC, hours_remaining ASC, minites_remaining ASC, seconds_remaining ASC;
