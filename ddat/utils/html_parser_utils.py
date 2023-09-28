""" Collection of custom HTML parsing utility functions for Python. """

from selenium.webdriver.common.by import By


def ul_to_list(ul_elem):
    """ Load a Python list with the contents of an unordered list HTML element.

    Args:
         ul_elem: HTML UL element.

    Returns:
        List containing the contents of the unordered list HTML element.

    """

    ul_list = []
    li_elems = ul_elem.find_elements(By.TAG_NAME, "li")
    for li_elem in li_elems:
        ul_list.append(li_elem.text)
    return ul_list
