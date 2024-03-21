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
	END//

DELIMITER ;