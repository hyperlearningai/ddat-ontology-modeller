#!/usr/bin/env python3
"""
DDaT profession capability framework website parser and modeller main program.
Usage: main.py
"""

import ddat.utils.yaml_utils as yaml_utils
import ddat.pipeline.setup as setup
import ddat.pipeline.parsers.skills_parser as skills_parser
import ddat.pipeline.parsers.roles_parser as roles_parser
import ddat.pipeline.modellers.ontology_modeller as ontology_modeller


# Application configuration.
config = yaml_utils.read_yaml('./ddat/config/config.yaml')
config_chromedriver = config['app']['webdrivers']['chromedriver']
config_ddat = config['ddat']
config_base_working_dir = config['app']['base_working_dir']

# Ontology model.
model_dir_path = './ddat/model/'

# Toggle pipeline modules to run.
run_module_setup = True
run_module_parser_skills = True
run_module_parser_roles = True
run_module_modeller_ontology = True

# Run the environment setup pipeline module.
if run_module_setup:
    print(f'Running the {setup.MODULE_NAME} module...')
    setup.setup_environment(config_base_working_dir)
    print(f'Finished running the {setup.MODULE_NAME} module.')

# Run the skills parser pipeline module.
if run_module_parser_skills:
    print(f'Running the {skills_parser.MODULE_NAME} module...')
    skills_parser.run(
        driver_path=config_chromedriver['driver'],
        ddat_base_url=config_ddat['base_url'],
        ddat_skills_resource=config_ddat['resources']['skills'],
        base_working_dir=config_base_working_dir)
    print(f'Finished running the {skills_parser.MODULE_NAME} module.')

# Run the roles parser pipeline module
if run_module_parser_roles:
    print(f'Running the {roles_parser.MODULE_NAME} module...')
    roles_parser.run(
        model_dir_path=model_dir_path,
        driver_path=config_chromedriver['driver'],
        ddat_base_url=config_ddat['base_url'],
        base_working_dir=config_base_working_dir)
    print(f'Finished running the {roles_parser.MODULE_NAME} module.')

# Run the ontology modeller pipeline module.
if run_module_modeller_ontology:
    print(f'Running the {ontology_modeller.MODULE_NAME} module...')
    ontology_modeller.run(
        model_dir_path=model_dir_path,
        base_working_dir=config_base_working_dir,
        ddat_base_url=config_ddat['base_url'],
        ddat_skills_resource=config_ddat['resources']['skills'])
    print(f'Finished running the {ontology_modeller.MODULE_NAME} module.')
