#!/usr/bin/env python3
"""
DDaT profession capability framework website parser and modeller main program.
Usage: main.py
"""

import ddat.utils.yaml_utils as yaml_utils
import ddat.pipeline.setup as setup
import ddat.pipeline.parsers.skills_parser as skills_parser
import ddat.pipeline.parsers.roles_parser as roles_parser
import ddat.pipeline.models.ontology.ontology_modeller as ontology_modeller
import ddat.pipeline.models.semantic_similarity.duplicate_skills_detector as duplicate_skills_detector

from ddat.config.logging_config import logger


# Application configuration.
config = yaml_utils.read_yaml('./ddat/config/config.yaml')
config_base_working_dir = config['app']['base_working_dir']
config_ddat = config['ddat']
config_pipeline = config['app']['pipeline']
config_webdriver_path = config['app']['webdriver_paths']['chromedriver']


# Ontology model.
ontology_model_dir_path = './ddat/model/ontology/'


# Start the application.
logger.info('Started DDaT Ontology Modeller.')
try:

    # Run the environment setup pipeline module.
    logger.info(f'Running the {setup.MODULE_NAME} module...')
    setup.setup_environment(config_base_working_dir)
    logger.info(f'Finished running the {setup.MODULE_NAME} module.')

    # Run the skills parser pipeline module.
    if config_pipeline['parsers']['skills']['enabled']:
        logger.info(f'Running the {skills_parser.MODULE_NAME} module...')
        skills_parser.run(
            driver_path=config_webdriver_path,
            ddat_base_url=config_ddat['base_url'],
            ddat_skills_resource=config_ddat['resources']['skills'],
            base_working_dir=config_base_working_dir)
        logger.info(f'Finished running the {skills_parser.MODULE_NAME} module.')

    # Run the roles parser pipeline module
    if config_pipeline['parsers']['roles']['enabled']:
        logger.info(f'Running the {roles_parser.MODULE_NAME} module...')
        roles_parser.run(
            ontology_model_dir_path=ontology_model_dir_path,
            driver_path=config_webdriver_path,
            ddat_base_url=config_ddat['base_url'],
            base_working_dir=config_base_working_dir)
        logger.info(f'Finished running the {roles_parser.MODULE_NAME} module.')

    # Run the ontology modeller pipeline module.
    if config_pipeline['models']['ontology']['enabled']:
        logger.info(f'Running the {ontology_modeller.MODULE_NAME} module...')
        ontology_modeller.run(
            ontology_model_dir_path=ontology_model_dir_path,
            base_working_dir=config_base_working_dir,
            ddat_base_url=config_ddat['base_url'],
            ddat_skills_resource=config_ddat['resources']['skills'],
            visualisation_apply_filters=config_pipeline['models']['ontology']['visualisation_apply_filters'])
        logger.info(f'Finished running the {ontology_modeller.MODULE_NAME} module.')

    # Run the duplicate skills detector pipeline module.
    if config_pipeline['models']['semantic_similarity']['skills']['enabled']:
        logger.info(f'Running the {duplicate_skills_detector.MODULE_NAME} module...')
        duplicate_skills_detector.run(base_working_dir=config_base_working_dir)
        logger.info(f'Finished running the {duplicate_skills_detector.MODULE_NAME} module.')


except Exception as e:

    logger.error('An error was encountered: \n' + repr(e))
    logger.error('Please consult the application logs for further information.')

finally:

    logger.info('Stopped DDaT Ontology Modeller.\n')
