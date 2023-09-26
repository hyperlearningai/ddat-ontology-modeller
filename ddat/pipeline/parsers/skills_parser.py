""" Skills parser pipeline module. """

import pickle

from ddat.classes.skill import Skill
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Module name.
MODULE_NAME = 'Skills Parser'

# Output file relative path and name.
OUTPUT_FILE_PATH = 'parsed/skills.pkl'

# CSS selectors.
SELECTOR_SKILLS_RESOURCE_HEADING = "h1.govuk-heading-xl"
SELECTOR_SKILLS_SHOW_ALL_SECTIONS_BUTTON = "button.govuk-accordion__show-all"
SELECTOR_SKILLS_ACCORDION_SECTIONS = "div.govuk-accordion__section--expanded"
SELECTOR_SKILL_CONTENT_SECTION = "div.govuk-accordion__section-content"
SELECTOR_SKILL_LEVEL_TABLE = "table.govuk-table"
SELECTOR_SKILL_LEVEL_TABLE_BODY = "tbody.govuk-table__body"
SELECTOR_SKILL_LEVEL_TABLE_BODY_ROW = "tr.govuk-table__row:nth-child(2n+1)"
SELECTOR_SKILL_LEVEL_TABLE_BODY_ROW_CELL = "td.govuk-table__cell"

# Wait and timeout durations.
IMPLICIT_WAIT = 5


def run(driver_path, ddat_base_url, ddat_skills_resource, base_working_dir):
    """  Run this pipeline module. 
    
    Args:
        driver_path (string): Path to the web driver.
        ddat_base_url (string): Base URL to the DDaT profession capability framework website.
        ddat_skills_resource (string): Relative URL to the DDaT skills resource.
        base_working_dir (string): Path to the base working directory.
    
    """
    
    # Open a browser and return a web driver instance.
    print('Opening a headless web driver instance.')
    driver = open_browser(driver_path, ddat_base_url, ddat_skills_resource)
    
    try:
        
        # Parse all the skills in the DDaT professional capability framework.
        print('Parsing all skills...')
        skills = parse_all_skills(driver)
        print('Parsing finished.')

        # Write the list of parsed Skill objects to file
        write_skills_to_file(skills, base_working_dir)
        
    finally:
        
        # Close the web driver instance.
        print('Closing the web driver instance.')
        close_driver(driver)


def open_browser(driver_path, ddat_base_url, ddat_skills_resource):
    """ Open a browser and return a Selenium driver instance.
    
    Args:
        driver_path (string): Path to the web driver.
        ddat_base_url (string): Base URL to the DDaT profession capability framework website.
        ddat_skills_resource (string): Relative URL to the DDaT skills resource.
        
    Returns:
        Selenium driver instance.
    
    """
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(driver_path, chrome_options=chrome_options)
    driver.implicitly_wait(IMPLICIT_WAIT)
    driver.get(f'{ddat_base_url}/{ddat_skills_resource}')
    return driver


def parse_all_skills(driver):
    """ Parse all DDaT skills.

    Args:
        driver: Selenium driver instance.

    Returns:
        List of Skill objects

    """

    # Press the 'Show all sections' button and wait
    show_all_sections_button_elem = driver.find_element(By.CSS_SELECTOR, SELECTOR_SKILLS_SHOW_ALL_SECTIONS_BUTTON)
    show_all_sections_button_elem.click()

    # Iterate over all skill accordion sections and create corresponding Skill objects
    skills = []
    skill_section_elems = driver.find_elements(By.CSS_SELECTOR, SELECTOR_SKILLS_ACCORDION_SECTIONS)
    for skill_section_elem in skill_section_elems:

        # Parse the skill name
        skill_name_elem = skill_section_elem.find_elements(By.TAG_NAME, "span")[2]

        # Parse the skill description
        skill_content_elem = skill_section_elem.find_element(By.CSS_SELECTOR, SELECTOR_SKILL_CONTENT_SECTION)
        skill_description_elem = skill_content_elem.find_element(By.TAG_NAME, "p")

        # Parse the skill levels
        skill_levels = {}
        skill_table_elem = skill_content_elem.find_element(By.CSS_SELECTOR, SELECTOR_SKILL_LEVEL_TABLE)
        skill_table_body_elem = skill_table_elem.find_element(By.CSS_SELECTOR, SELECTOR_SKILL_LEVEL_TABLE_BODY)
        skill_table_body_row_elems = skill_table_body_elem.find_elements(
            By.CSS_SELECTOR, SELECTOR_SKILL_LEVEL_TABLE_BODY_ROW)
        for skill_table_body_row_elem in skill_table_body_row_elems:
            skill_table_body_row_cell_elems = skill_table_body_row_elem.find_elements(
                By.CSS_SELECTOR, SELECTOR_SKILL_LEVEL_TABLE_BODY_ROW_CELL)
            skill_level_cell_elem = skill_table_body_row_cell_elems[0]
            skill_level_capabilities_cell_elem = skill_table_body_row_cell_elems[1]

            # Parse the skill level for the current row
            skill_level_elem = skill_level_cell_elem.find_element(By.TAG_NAME, "p")

            # Parse the skill level capabilities for the current row
            skill_level_capabilities = []
            skill_level_capability_elems = skill_level_capabilities_cell_elem.find_elements(By.TAG_NAME, "li")
            for skill_level_capability_elem in skill_level_capability_elems:
                skill_level_capabilities.append(skill_level_capability_elem.text)

            # Insert this skill level <> capability mapping into the skill levels dictionary
            skill_levels[skill_level_elem.text] = skill_level_capabilities

        # Create a Skill object for this skill
        skill = Skill(
            anchor_id=skill_name_elem.get_attribute('id'),
            name=skill_name_elem.text,
            description=skill_description_elem.text,
            skill_levels=skill_levels
        )

        # Add this new Skill object to the list of Skills
        skills.append(skill)

    return skills


def write_skills_to_file(skills, base_working_dir):
    """  Write the list of parsed Skill objects to file.

    Args:
        skills (list): List of parsed Skill objects.
        base_working_dir (string): Path to the base working directory.

    """

    with open(f'{base_working_dir}/{OUTPUT_FILE_PATH}', 'wb') as f:
        pickle.dump(skills, f)


def close_driver(driver):
    """ Close a Selenium driver instance. """
    driver.quit()
