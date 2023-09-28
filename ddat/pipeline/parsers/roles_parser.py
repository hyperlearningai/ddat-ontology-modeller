""" Roles parser pipeline module. """

import ddat.utils.html_parser_utils as html_parser_utils
import ddat.utils.string_utils as string_utils
import json
import pickle

from ddat.classes.role import Role
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
HTML_CHANGELOG_UL_CLASS_NAME = "roles-changelog"
HTML_SMALL_PARAGRAPH_CLASS_NAME = "govuk-body-s"

# Content templates.
CONTENT_ROLE_RESPONSIBILITIES_PRECEDING_TEXT = "At this role level, you will"
CONTENT_CIVIL_SERVICE_JOB_GRADES_PRECEDING_TEXT = "This role level is often performed at the"

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
    print('Opening a headless web driver instance...')
    driver = open_browser(driver_path, ddat_base_url)

    try:

        # Parse all the roles in the DDaT professional capability framework.
        print('Parsing all roles...')
        roles = parse_all_roles(driver, class_branches)
        print('Parsing finished.')

        # Write the list of parsed Role objects to file
        write_roles_to_file(roles, base_working_dir)

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
    for class_branch in class_branches:

        # Navigate to the branch resource
        driver.get(f'{class_branch.url}')

        # Parse the list of roles associated with this branch
        role_link_elems = driver.find_elements(By.CSS_SELECTOR, SELECTOR_ROLE_LINKS)
        number_roles = len(role_link_elems)
        number_roles_processed = 0
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

            # Locate all paragraphs that are siblings (i.e. excluding those in the skills table) of the
            # role level header which are between the current role level header and the next role level header.
            role_paragraph_sibling_elems = driver.find_elements(
                By.XPATH, f'//p[preceding-sibling::h3[@id="{role_url_anchor_id}"] '
                          f'and count(following-sibling::h3)={number_roles - (number_roles_processed + 1)} '
                          f'and not(contains(@class, "{HTML_SMALL_PARAGRAPH_CLASS_NAME}"))]')

            # Get the role description (as the 1st paragraph after the role level header).
            # Note that even if the role description is missing on the webpage,
            # an empty <p class="govuk-body"></p> is still rendered as part of the DOM.
            # This means that role_description will be an empty string object in this case.
            role_description = role_paragraph_sibling_elems[0].text

            # Locate all the unordered lists that are siblings (i.e. excluding those in the skills table) of the
            # role level header which are between the current role level header and the next role level header.
            role_ul_sibling_elems = driver.find_elements(
                By.XPATH, f'//ul[preceding-sibling::h3[@id="{role_url_anchor_id}"] '
                          f'and count(following-sibling::h3)={number_roles - (number_roles_processed + 1)} '
                          f'and not(contains(@class, "{HTML_CHANGELOG_UL_CLASS_NAME}"))]')
            number_ul_siblings = len(role_ul_sibling_elems)

            # If there are two unordered list siblings, then both the list of responsibilities
            # and list of civil service job grades are available for this role.
            role_responsibilities = []
            role_civil_service_job_grades = []
            if number_ul_siblings == 2:

                # Get the list of role responsibilities (as the 1st unordered list)
                role_responsibilities = html_parser_utils.ul_to_list(role_ul_sibling_elems[0])

                # Get the list of civil service job grades (as the 2nd unordered list)
                role_civil_service_job_grades = html_parser_utils.ul_to_list(role_ul_sibling_elems[1])

            # If there is only one unordered list, then determine whether it is the list of role responsibilities
            # or the list of civil service job grades by examining the contents of the paragraphs parsed earlier.
            elif number_ul_siblings == 1:
                for role_paragraph_sibling_elem in role_paragraph_sibling_elems:

                    # Get the list of role responsibilities (as the 1st and only unordered list)
                    if CONTENT_ROLE_RESPONSIBILITIES_PRECEDING_TEXT in role_paragraph_sibling_elem.text:
                        role_responsibilities = html_parser_utils.ul_to_list(role_ul_sibling_elems[0])
                        break

                    # Get the list of civil service job grades (as the 1st and only unordered list)
                    elif CONTENT_CIVIL_SERVICE_JOB_GRADES_PRECEDING_TEXT in role_paragraph_sibling_elem.text:
                        role_civil_service_job_grades = html_parser_utils.ul_to_list(role_ul_sibling_elems[0])
                        break

            # Locate the skills table and its rows of skills
            role_skill_table_css_selector = f'{role_heading_css_selector} ~ table'
            role_skill_table_elem = driver.find_element(By.CSS_SELECTOR, role_skill_table_css_selector)
            role_skill_table_th_css_selector = f'tbody > tr > th'
            role_skill_table_th_elems = role_skill_table_elem.find_elements(
                By.CSS_SELECTOR, role_skill_table_th_css_selector)

            # Get the dictionary of skills
            role_skills = {}
            for role_skill_table_th_elem in role_skill_table_th_elems:
                role_skill_table_th_p_elems = role_skill_table_th_elem.find_elements(By.TAG_NAME, 'p')
                role_skill_name_link_elem = role_skill_table_th_p_elems[0].find_element(By.TAG_NAME, 'a')
                role_skill_name = role_skill_name_link_elem.text
                role_skill_iri_id = string_utils.pascal_case(role_skill_name)
                role_skill_level = role_skill_table_th_p_elems[1].text
                role_skills[role_skill_iri_id] = string_utils.clean_skill_level(role_skill_level)

            # Create a Role object for this role
            role = Role(
                name=role_name,
                branch_id=class_branch.id,
                description=role_description,
                url=role_url,
                responsibilities=role_responsibilities,
                civil_service_job_grades=role_civil_service_job_grades)
            role.set_skills(role_skills)

            # Add this new Role object to the list of Roles
            roles.append(role)

            # Increment the number of roles processed counter
            number_roles_processed += 1

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
