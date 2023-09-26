#!/usr/bin/env python3
""" Collection of string utility functions for Python. """


def camel_case(text):
    """ Converts a given string into camel case.

    Args:
        text (string): String to convert.

    Returns:
        String converted to camel case.

    """

    camel_case_str = ''.join(c for c in text.title() if c.isalnum())
    return camel_case_str[0].lower() + camel_case_str[1:]