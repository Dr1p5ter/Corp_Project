# Code was adopted by nguyenkims using this link :
# link = https://gist.github.com/nguyenkims/e92df0f8bd49973f0c94bddf36ed7fd0
# I made a few edits

import logging
import sys
from logging.handlers import TimedRotatingFileHandler

FORMATTER = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s")
LOG_FILE = "admin_service.log"

def get_console_handler():
	console_handler = logging.StreamHandler(sys.stdout)
	console_handler.setFormatter(FORMATTER)
	return console_handler

def get_file_handler():
	file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
	file_handler.setFormatter(FORMATTER)
	return file_handler

def get_logger(logger_name):
	logger = logging.getLogger(logger_name)

	logger.setLevel(logging.DEBUG) # better to have too much log than not enough

	logger.addHandler(get_console_handler())
	logger.addHandler(get_file_handler())

	# with this pattern, it's rarely necessary to propagate the error up to parent
	logger.propagate = False

	return logger

logger = get_logger(LOG_FILE)