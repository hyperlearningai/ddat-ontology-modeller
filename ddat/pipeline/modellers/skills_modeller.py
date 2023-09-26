#!/usr/bin/env python3
""" Skills modeller pipeline module. """

import ddat.utils.string_utils as string_utils
import pickle

from ddat.classes.skill import Skill

# Module name.
MODULE_NAME = 'Skills Modeller'

# Input file relative path and name.
INPUT_FILE_PATH = 'parsed/skills.pkl'

# Output file relative path and name.
OUTPUT_FILE_PATH = 'modelled/skills.xml'

# OWL RDF/XML substrings.
SKILL_IRI_ANCHOR_PREFIX = '#skill'


def run(ddat_base_url, ddat_skills_resource, base_iri, base_working_dir):
    """ Run this pipeline module.

    Args:
        ddat_base_url (string): Base URL to the DDaT profession capability framework website.
        ddat_skills_resource (string): Relative URL to the DDaT skills resource.
        base_iri (string): Base IRI for OWL classes.
        base_working_dir (string): Path to the base working directory.

    """

    # Read the list of parsed Skill objects from file
    skills = read_skills_from_file(base_working_dir)

    # Model the list of parsed Skill objects
    modelled_skills = model_skills(skills, ddat_base_url, ddat_skills_resource, base_iri)

    # Write the list of modelled Skill classes to file
    write_modelled_skills_to_file(modelled_skills, base_working_dir)


def read_skills_from_file(base_working_dir):
    """ Read the list of parsed Skill objects from file.

    Args:
        base_working_dir (string): Path to the base working directory.

    Returns:
        List of parsed Skill objects.

    """

    with open(f'{base_working_dir}/{INPUT_FILE_PATH}', 'rb') as f:
        skills = pickle.load(f)
    return skills


def model_skills(skills, ddat_base_url, ddat_skills_resource, base_iri):
    """ Model the list of parsed Skill objects.

    Args:
        skills (list): List of parsed Skill objects.
        ddat_base_url (string): Base URL to the DDaT profession capability framework website.
        ddat_skills_resource (string): Relative URL to the DDaT skills resource.
        base_iri (string): Base IRI for OWL classes.

    Returns:
        List of modelled Skill classes.

    """

    modelled_skills = []
    for skill in skills:
        modelled_skill = model_skill(skill, ddat_base_url, ddat_skills_resource, base_iri)
        modelled_skills.append(modelled_skill)
    return modelled_skills


def model_skill(skill, ddat_base_url, ddat_skills_resource, base_iri):
    """ Model a Skill object as an OWL RDF/XML class.

    Args:
        skill (Skill): Skill object.
        ddat_base_url (string): Base URL to the DDaT profession capability framework website.
        ddat_skills_resource (string): Relative URL to the DDaT skills resource.
        base_iri (string): Base IRI for OWL classes.

    Returns:
        XML string modelling the Skill object as an OWL RDF/XML class

    """

    return f'''
        <owl:Class rdf:about="{base_iri}{SKILL_IRI_ANCHOR_PREFIX}{string_utils.pascal_case(skill.name)}">
            <rdfs:label xml:lang="en">{skill.name}</rdfs:label>
            <skos:definition xml:lang="en" rdf:datatype="http://www.w3.org/2001/XMLSchema#string">{skill.description}</skos:definition>
            <entityType xml:lang="en" rdf:datatype="http://www.w3.org/2001/XMLSchema#string">Skill</entityType>
            <url xml:lang="en" rdf:resource="{ddat_base_url}/{ddat_skills_resource}#{skill.anchor_id}"/>
        </owl:Class>'''


def write_modelled_skills_to_file(modelled_skills, base_working_dir):
    """ Write the list of modelled Skill classes to file.

    Args:
        modelled_skills (list):  List of modelled Skill classes.
        base_working_dir (string): Path to the base working directory.

    """

    with open(f'{base_working_dir}/{OUTPUT_FILE_PATH}', 'w') as f:
        for modelled_skill in modelled_skills:
            f.write(f'{modelled_skill}\n')
