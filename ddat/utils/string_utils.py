""" Collection of custom string utility functions for Python. """


def camel_case(text):
    """ Converts a given string into camel case.

    Args:
        text (string): String to convert.

    Returns:
        String converted to camel case.

    """

    camel_case_str = ''.join(c for c in text.title() if c.isalnum())
    return camel_case_str[0].lower() + camel_case_str[1:]


def pascal_case(text):
    """ Converts a given string into pascal case.

    Args:
        text (string): String to convert.

    Returns:
        String converted to pascal case.

    """

    pascal_case_str = ''.join(c for c in text.title() if c.isalnum())
    return pascal_case_str[0].upper() + pascal_case_str[1:]


def remove_ordered_list_prefix(text):
    """ Remove the initial number and period prefix from a string.

    Args:
        text (string): String to transform.

    Returns:
        String with the initial number and period removed

    """

    return text.lstrip('0123456789. ')


def clean_skill_level(raw_skill_level):
    """ Remove the 'Level: ' prefix and capitalize.

    Args:
        raw_skill_level (string): Raw skill level

    Returns:
        Cleansed skill level string

    """

    return raw_skill_level.removeprefix('Level: ').upper()


def list_to_ordered_list_string(input_list):
    """ Convert a list of strings into a string ordered list.

    Args:
        input_list (list): List of strings

    Returns:
        String ordered list.

    """

    ordered_list_string = ''
    counter = 1
    for item in input_list:
        ordered_list_string += f'{counter}. {item[0].upper()}{item[1:]}. \n'
        counter += 1
    return ordered_list_string
