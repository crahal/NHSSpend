import datetime
import json
import logging
import logging.config
import os

root_logger = logging.getLogger('pdf_table_parser')
logger = logging.getLogger('pdf_table_parser').getChild(__name__)

file_path = os.path.dirname(os.path.realpath(__file__))
project_path = file_path
log_path = os.path.join(project_path, 'log')
logging_config_filename = os.path.join(file_path, 'log_config.json')


def logging_setup():
	# This should not be neccessary but pdfminer3k does not log properly
	# Supressing propagation stops the duplication of our log messages
	# Setting the root logger to error stops its warning spam
	logging.propagate = False
	logging.getLogger().setLevel(logging.ERROR)
	if not root_logger.hasHandlers():
		try:
			with open(logging_config_filename, 'r') as file:
				config_dict = json.load(file)
				time_stamp_string = datetime.datetime.now().isoformat().replace(':', '.')
				time_stamp_filename = config_dict['handlers']['file']['filename'].replace('%', time_stamp_string)
				config_dict['handlers']['file']['filename'] = os.path.join(log_path, time_stamp_filename)
				logging.config.dictConfig(config_dict)
		except EnvironmentError:
			logger.error('Logging config is missing, please provide {logging_config_filename} before continuing'.format(**locals()))
			raise
	logger.info('Log file initialised')
