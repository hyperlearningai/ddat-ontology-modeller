""" Roles parser pipeline module. """

import json
import pickle

from ddat.classes.role import Role
import ddat.utils.string_utils as string_utils
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from types import SimpleNamespace

# Module name.
MODULE_NAME = 'Roles Parser'

# Input model file names.
INPUT_MODEL_CLASS_BRANCHES_FILE_NAME = 'class_branches.json'

# Output file relative path and name.
OUTPUT_FILE_PATH = 'parsed/roles.pkl'

# CSS selectors.
SELECTOR_ROLE_LINKS = "ul.contents-list-links.indented-list > li > a"

# HTML classes.
HTML_ROLE_LEVEL_HEADER_CLASS_NAME = "role-level-header"

# Wait and timeout durations.
IMPLICIT_WAIT = 5


def run(model_dir_path, driver_path, ddat_base_url, base_working_dir):
    """  Run this pipeline module.

    Args:
        model_dir_path (string): Path to the directory holding the ontology model.
        driver_path (string): Path to the web driver.
        ddat_base_url (string): Base URL to the DDaT profession capability framework website.
        base_working_dir (string): Path to the base working directory.

    """

    # Load the pre-defined branch classes from the ontology model.
    class_branches = load_class_branches(model_dir_path)

    # Open a browser and return a web driver instance.
    print('Opening a headless web driver instance.')
    driver = open_browser(driver_path, ddat_base_url)

    try:

        # Parse all the roles in the DDaT professional capability framework.
        print('Parsing all roles...')
        roles = parse_all_roles(driver, class_branches)
        print('Parsing finished.')

        # Write the list of parsed Role objects to file
        # write_roles_to_file(roles, base_working_dir)

    finally:

        # Close the web driver instance.
        print('Closing the web driver instance.')
        close_driver(driver)


def load_class_branches(model_dir_path):
    """ Load the pre-defined branch classes from the ontology data model.

    Args:
        model_dir_path (string): Path to the directory holding the pre-defined ontology data model.

    Returns:
        List of branch class objects.

    """

    with open(f'{model_dir_path}/{INPUT_MODEL_CLASS_BRANCHES_FILE_NAME}', 'r') as f:
        class_branches = json.load(f, object_hook=lambda d: SimpleNamespace(**d))
    return class_branches


def open_browser(driver_path, ddat_base_url):
    """ Open a browser and return a Selenium driver instance.

    Args:
        driver_path (string): Path to the web driver.
        ddat_base_url (string): Base URL to the DDaT profession capability framework website.

    Returns:
        Selenium driver instance.

    """

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(driver_path, chrome_options=chrome_options)
    driver.implicitly_wait(IMPLICIT_WAIT)
    driver.get(f'{ddat_base_url}')
    return driver


def parse_all_roles(driver, class_branches):
    """ Parse all DDaT skills.

    Args:
        driver: Selenium driver instance.
        class_branches (list): List of pre-defined branch class objects.

    Returns:
        List of Role objects

    """

    # Iterate over all class branches
    roles = []
    x = 1
    for class_branch in class_branches:
        if x < 2:
            x += 1

            # Navigate to the branch resource
            driver.get(f'{class_branch.url}')

            # Parse the list of roles associated with this branch
            role_link_elems = driver.find_elements(By.CSS_SELECTOR, SELECTOR_ROLE_LINKS)
            for role_link_elem in role_link_elems:

                # Get the role URL
                role_url = role_link_elem.get_attribute('href')

                # Extract the anchor ID from the URL
                role_url_anchor_id = role_url.split("#")[1]

                # Locate the role level header with the anchor ID
                role_heading_css_selector = f'h3#{role_url_anchor_id}.{HTML_ROLE_LEVEL_HEADER_CLASS_NAME}'
                role_heading_elem = driver.find_element(By.CSS_SELECTOR, role_heading_css_selector)

                # Get the role name and clean (remove the initial number and period prefix, and title)
                role_name = string_utils.remove_ordered_list_prefix(role_heading_elem.text).title()

                # Locate the first paragraph immediately after the role level header
                role_description_css_selector = f'{role_heading_css_selector} + p'
                role_description_elem = driver.find_element(By.CSS_SELECTOR, role_description_css_selector)

                # Get the role description
                role_description = role_description_elem.text

                # Locate the role unordered list elements after the role level header
                role_lists_css_selector = f'{role_heading_css_selector} ~ ul'
                role_lists_elems = driver.find_elements(By.CSS_SELECTOR, role_lists_css_selector)

                # Get the role responsibilities (as the 1st bullet point list after the role level header)
                role_responsibilities = []
                role_responsibility_elems = role_lists_elems[0].find_elements(By.TAG_NAME, "li")
                for role_responsibility_elem in role_responsibility_elems:
                    role_responsibilities.append(role_responsibility_elem.text)

                # Get the list of civil service job grades (as the 2nd bullet point list after the role level header)
                role_civil_service_job_grades = []
                role_civil_service_job_grade_elems = role_lists_elems[1].find_elements(By.TAG_NAME, "li")
                for role_civil_service_job_grade_elem in role_civil_service_job_grade_elems:
                    role_civil_service_job_grades.append(role_civil_service_job_grade_elem.text)

                # Create a Role object for this role
                role = Role(
                    name=role_name,
                    branch_id=class_branch.id,
                    description=role_description,
                    url=role_url,
                    responsibilities=role_responsibilities,
                    civil_service_job_grades=role_civil_service_job_grades)

                # Add this new Role object to the list of Roles
                roles.append(role)

    return roles


def write_roles_to_file(roles, base_working_dir):
    """  Write the list of parsed Role objects to file.

    Args:
        roles (list): List of parsed Role objects.
        base_working_dir (string): Path to the base working directory.

    """

    with open(f'{base_working_dir}/{OUTPUT_FILE_PATH}', 'wb') as f:
        pickle.dump(roles, f)


def close_driver(driver):
    """ Close a Selenium driver instance. """
    driver.quit()
