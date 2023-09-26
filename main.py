#!/usr/bin/env python3
""" DDaT profession capability framework parsers main pipeline. """

import ddat.utils.yaml_utils as yaml_utils
import ddat.pipeline.setup as setup
import ddat.pipeline.parsers.skills_parser as skills_parser
import ddat.pipeline.modellers.skills_modeller as skills_modeller


# Application configuration.
config = yaml_utils.read_yaml('./ddat/config/config.yaml')
config_chromedriver = config['app']['webdrivers']['chromedriver']
config_ddat = config['ddat']
config_base_working_dir = config['app']['base_working_dir']

# Toggle pipeline modules to run.
run_module_setup = True
run_module_parser_skills = True
run_module_modeller_skills = True

# Run the environment setup pipeline module.
if run_module_setup:
    print(f'Running the {setup.MODULE_NAME} module...')
    setup.setup_environment(config_base_working_dir)
    print(f'Finished running the {setup.MODULE_NAME} module.')

# Run the skills parsers pipeline module.
if run_module_parser_skills:
    print(f'Running the {skills_parser.MODULE_NAME} module...')
    skills_parser.run(
        driver_path=config_chromedriver['driver'],
        ddat_base_url=config_ddat['base_url'],
        ddat_skills_resource=config_ddat['resources']['skills'],
        base_working_dir=config_base_working_dir)
    print(f'Finished running the {skills_parser.MODULE_NAME} module.')

# Run the skills modeller pipeline module.
if run_module_modeller_skills:
    print(f'Running the {skills_modeller.MODULE_NAME} module...')
    skills_modeller.run(
        ddat_base_url=config_ddat['base_url'],
        ddat_skills_resource=config_ddat['resources']['skills'],
        base_iri=config_ddat['ontology']['base_iri'],
        base_working_dir=config_base_working_dir)
    print(f'Finished running the {skills_modeller.MODULE_NAME} module.')
