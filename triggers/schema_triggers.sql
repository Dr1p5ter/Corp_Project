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
        SET NEW.date_to_clean_strikes = DATE_ADD(NOW(), INTERVAL 7 DAY);
	ELSEIF NEW.strike_count = 2 THEN
		SET NEW.text_coms_friend = FALSE;
        SET NEW.voice_coms_friend = FALSE;
        SET NEW.last_strike_made = NOW();
        SET NEW.date_to_clean_strikes = DATE_ADD(NOW(), INTERVAL 14 DAY);
	ELSEIF NEW.strike_count > 2 THEN
		SET NEW.last_strike_made = NOW();
        SET NEW.date_to_clean_strikes = DATE_ADD(NOW(), INTERVAL 6 MONTH);
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