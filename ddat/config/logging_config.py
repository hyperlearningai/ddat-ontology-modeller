""" Logging configuration. """

import ddat.utils.yaml_utils as yaml_utils
import logging
import os


# Application configuration.
config = yaml_utils.read_yaml('./ddat/config/config.yaml')
config_base_working_dir = config['app']['base_working_dir']

# Create the logs directory if it does not already exist.
os.makedirs(f'{config_base_working_dir}/logs', exist_ok=True)

# Create the logger
logger = logging.getLogger('DDaT Ontology Modeller')
logger.setLevel(logging.DEBUG)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# File handler
file_handler = logging.FileHandler(f'{config_base_working_dir}/logs/application.log')
file_handler.setLevel(logging.DEBUG)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
