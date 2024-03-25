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
