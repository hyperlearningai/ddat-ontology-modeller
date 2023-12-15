""" Environment setup pipeline module. """

import os

MODULE_NAME = 'Setup'
required_working_dirs = ['logs', 'models', 'models/ontology', 'models/semantic_similarity', 'parsed']


def setup_environment(base_working_dir):
    """  Set up the environment.
    
    Args:
        base_working_dir (string): Path to the base working directory.
    
    """
    
    # Create the required working directories.
    if not os.path.exists(f'{base_working_dir}'):
        os.mkdir(f'{base_working_dir}')
    for required_working_dir in required_working_dirs:
        if not os.path.exists(f'{base_working_dir}/{required_working_dir}'):
            os.mkdir(f'{base_working_dir}/{required_working_dir}')
    