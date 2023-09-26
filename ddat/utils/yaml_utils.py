""" Collection of custom YAML utility functions for Python. """

import yaml


def read_yaml(file_path):
    """ Read a given YAML file. 
    
    Args:
        file_path (string): YAML file path.
        
    Returns:
        Python object.
    
    """
    
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)
