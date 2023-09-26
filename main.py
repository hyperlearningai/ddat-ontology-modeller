#!/usr/bin/env python3
""" DDaT profession capability framework parser main pipeline. """

import ddat.utils.yaml_utils as yaml_utils
import ddat.pipeline.setup as setup
import ddat.pipeline.parser.parser as parser


# Application configuration.
config = yaml_utils.read_yaml('./ddat/config/config.yaml')
config_chromedriver = config['app']['webdrivers']['chromedriver']
config_ddat = config['ddat']
config_base_output_dir = config['app']['base_output_dir']

# Toggle pipeline modules to run.
run_module_setup = True
run_module_parser = True

# Run the environment setup pipeline module.
if run_module_setup:
    print(f'Running the {setup.MODULE_NAME} module...')
    setup.setup_environment(config_base_output_dir)

# Run the parser pipeline module.
if run_module_parser:
    print(f'Running the {parser.MODULE_NAME} module...')
    parser.run(
        driver_path=config_chromedriver['driver'],
        ddat_base_url=config_ddat['base_url'],
        ddat_skills_resource=config_ddat['resources']['skills'],
        base_output_dir=config_base_output_dir)
