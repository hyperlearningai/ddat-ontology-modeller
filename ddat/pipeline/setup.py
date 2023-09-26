#!/usr/bin/env python3
""" Environment setup pipeline module. """

import os

MODULE_NAME = 'Setup'
required_working_dirs = ['classes', 'working']


def setup_environment(base_output_dir):
    """  Set up the environment.
    
    Args:
        base_output_dir (string): Path to the base output directory.
    
    """
    
    # Create the required working directories.
    for required_working_dir in required_working_dirs:
        if not os.path.exists(f'{base_output_dir}/{required_working_dir}'):
            os.mkdir(f'{base_output_dir}/{required_working_dir}')
    