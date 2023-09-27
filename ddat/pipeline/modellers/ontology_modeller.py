""" Ontology modeller pipeline module. """

import ddat.utils.string_utils as string_utils
import json
import pickle

from ddat.classes.ontology import Ontology
from types import SimpleNamespace

# Module name.
MODULE_NAME = 'Ontology Modeller'

# Input model file names.
INPUT_MODEL_ONTOLOGY_METADATA_FILE_NAME = 'ontology_metadata.json'
INPUT_MODEL_ANNOTATION_PROPERTIES_FILE_NAME = 'annotation_properties.json'
INPUT_MODEL_OBJECT_PROPERTIES_FILE_NAME = 'object_properties.json'
INPUT_MODEL_CLASS_THINGS_FILE_NAME = 'class_things.json'
INPUT_MODEL_CLASS_DISCIPLINES_FILE_NAME = 'class_disciplines.json'
INPUT_MODEL_CLASS_BRANCHES_FILE_NAME = 'class_branches.json'

# Input parsed objects.
INPUT_SKILLS_FILE_PATH = 'parsed/skills.pkl'
INPUT_ROLES_FILE_PATH = 'parsed/roles.pkl'

# Output file relative path and name.
OUTPUT_FILE_PATH = 'modelled/ddat.owl'

# OWL RDF/XML substrings.
RDF_DATATYPE_STRING = 'rdf:datatype="http://www.w3.org/2001/XMLSchema#string"'
OWL_TOP_OBJECT_PROPERTY_IRI = 'rdf:resource="http://www.w3.org/2002/07/owl#topObjectProperty"'
OWL_SKILL_CLASS_ID = 'skill'

# Entity types.
ENTITY_TYPE_DISCIPLINE = 'Discipline'
ENTITY_TYPE_BRANCH = 'Branch'
ENTITY_TYPE_ROLE = 'Role'
ENTITY_TYPE_SKILL = 'Skill'


def run(model_dir_path, base_working_dir, ddat_base_url, ddat_skills_resource):
    """ Run this pipeline module.

    Args:
        model_dir_path (string): Path to the directory holding the ontology model.
        base_working_dir (string): Path to the base working directory.
        ddat_base_url (string): Base URL to the DDaT profession capability framework website.
        ddat_skills_resource (string): Relative URL to the DDaT skills resource.

    """

    # Load the pre-defined ontology metadata and create the initial Ontology object.
    ontology = load_ontology_metadata(model_dir_path)

    # Load the pre-defined annotation properties from the ontology data model.
    ontology = load_annotation_properties(ontology, model_dir_path)

    # Load the pre-defined object properties from the ontology data model.
    ontology = load_object_properties(ontology, model_dir_path)

    # Load the pre-defined thing classes from the ontology model.
    ontology = load_class_things(ontology, model_dir_path)

    # Load the pre-defined discipline classes from the ontology model.
    ontology = load_class_disciplines(ontology, model_dir_path)

    # Load the pre-defined branch classes from the ontology model.
    ontology = load_class_branches(ontology, model_dir_path)

    # Load the parsed Skill objects from file.
    ontology = load_class_skills(ontology, base_working_dir)

    # Model the Ontology as an OWL RDF/XML ontology.
    modelled_ontology = model_ontology(ontology, ddat_base_url, ddat_skills_resource)

    # Write the modelled ontology OWL RDF/XML string to file.
    write_ontology_to_file(modelled_ontology, base_working_dir)


def load_ontology_metadata(model_dir_path):
    """ Load the pre-defined ontology metadata and create the initial Ontology object.

    Args:
        model_dir_path (string): Path to the directory holding the pre-defined ontology data model.

    Returns:
        Ontology object.

    """

    with open(f'{model_dir_path}/{INPUT_MODEL_ONTOLOGY_METADATA_FILE_NAME}', 'r') as f:
        ontology_metadata = json.load(f, object_hook=lambda d: SimpleNamespace(**d))
    ontology = Ontology(
        name=ontology_metadata.name,
        iri=ontology_metadata.iri,
        description=ontology_metadata.description,
        owl_version=ontology_metadata.owl.version,
        contributors=ontology_metadata.contributors)
    return ontology


def load_annotation_properties(ontology, model_dir_path):
    """ Load the pre-defined annotation properties from the ontology data model.

    Args:
        ontology (Ontology): Ontology object
        model_dir_path (string): Path to the directory holding the pre-defined ontology data model.

    Returns:
        Ontology object.

    """

    with open(f'{model_dir_path}/{INPUT_MODEL_ANNOTATION_PROPERTIES_FILE_NAME}', 'r') as f:
        annotation_properties = json.load(f, object_hook=lambda d: SimpleNamespace(**d))
    ontology.set_annotation_properties(annotation_properties)
    return ontology


def load_object_properties(ontology, model_dir_path):
    """ Load the pre-defined object properties from the ontology data model.

    Args:
        ontology (Ontology): Ontology object
        model_dir_path (string): Path to the directory holding the pre-defined ontology data model.

    Returns:
        Ontology object.

    """

    with open(f'{model_dir_path}/{INPUT_MODEL_OBJECT_PROPERTIES_FILE_NAME}', 'r') as f:
        object_properties = json.load(f, object_hook=lambda d: SimpleNamespace(**d))
    ontology.set_object_properties(object_properties)
    return ontology


def load_class_things(ontology, model_dir_path):
    """ Load the pre-defined thing classes from the ontology data model.

    Args:
        ontology (Ontology): Ontology object
        model_dir_path (string): Path to the directory holding the pre-defined ontology data model.

    Returns:
        Ontology object.

    """

    with open(f'{model_dir_path}/{INPUT_MODEL_CLASS_THINGS_FILE_NAME}', 'r') as f:
        class_things = json.load(f, object_hook=lambda d: SimpleNamespace(**d))
    ontology.set_class_things(class_things)
    return ontology


def load_class_disciplines(ontology, model_dir_path):
    """ Load the pre-defined discipline classes from the ontology data model.

    Args:
        ontology (Ontology): Ontology object
        model_dir_path (string): Path to the directory holding the pre-defined ontology data model.

    Returns:
        Ontology object.

    """

    with open(f'{model_dir_path}/{INPUT_MODEL_CLASS_DISCIPLINES_FILE_NAME}', 'r') as f:
        class_disciplines = json.load(f, object_hook=lambda d: SimpleNamespace(**d))
    ontology.set_class_disciplines(class_disciplines)
    return ontology


def load_class_branches(ontology, model_dir_path):
    """ Load the pre-defined branch classes from the ontology data model.

    Args:
        ontology (Ontology): Ontology object
        model_dir_path (string): Path to the directory holding the pre-defined ontology data model.

    Returns:
        Ontology object.

    """

    with open(f'{model_dir_path}/{INPUT_MODEL_CLASS_BRANCHES_FILE_NAME}', 'r') as f:
        class_branches = json.load(f, object_hook=lambda d: SimpleNamespace(**d))
    ontology.set_class_branches(class_branches)
    return ontology


def load_class_skills(ontology, base_working_dir):
    """ Load the list of parsed Skill objects from file.

    Args:
        ontology (Ontology): Ontology object
        base_working_dir (string): Path to the base working directory.

    Returns:
        Ontology object.

    """

    with open(f'{base_working_dir}/{INPUT_SKILLS_FILE_PATH}', 'rb') as f:
        skills = pickle.load(f)
    ontology.set_class_skills(skills)
    return ontology


def model_ontology(ontology, ddat_base_url, ddat_skills_resource):
    """ Model an Ontology object as an OWL RDF/XML ontology.

    Args:
        ontology (Ontology): Ontology object
        ddat_base_url (string): Base URL to the DDaT profession capability framework website.
        ddat_skills_resource (string): Relative URL to the DDaT skills resource.

    Returns:
        Modelled ontology OWL RDF/XML string

    """

    return (f'{model_ontology_metadata(ontology)}'
            f'{model_annotation_properties(ontology)}'
            f'{model_object_properties(ontology)}'
            f'{model_class_things(ontology)}'
            f'{model_class_disciplines(ontology)}'
            f'{model_class_branches(ontology)}'
            f'{model_class_skills(ontology, ddat_base_url, ddat_skills_resource)}')


def model_ontology_metadata(ontology):
    """ Model metadata from an Ontology object as an OWL RDF/XML string.

    Args:
        ontology (Ontology): Ontology object

    Returns:
        Modelled ontology metadata OWL RDF/XML string

    """

    # Generate the contributors string.
    modelled_contributors = ''
    for contributor in ontology.contributors:
        modelled_contributors += f'<terms:contributor>{contributor}</terms:contributor>'

    return f'''<?xml version="1.0"?>
<rdf:RDF xmlns="{ontology.iri}#"
    xml:base="{ontology.iri}"
    xmlns:ddat="{ontology.iri}"
    xmlns:owl="http://www.w3.org/2002/07/owl#"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:xml="http://www.w3.org/XML/1998/namespace"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
    xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
    xmlns:skos="http://www.w3.org/2004/02/skos/core#"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:terms="http://purl.org/dc/terms/">\n\n
    <!-- ONTOLOGY METADATA -->\n\n
    <owl:Ontology rdf:about="{ontology.iri}">
        <dc:title xml:lang="en">{ontology.name}</dc:title>
        <rdfs:label xml:lang="en" {RDF_DATATYPE_STRING}>{ontology.name}</rdfs:label>
        {modelled_contributors}
        <dc:description xml:lang="en">{ontology.description}</dc:description>
        <owl:versionInfo {RDF_DATATYPE_STRING}>{ontology.owl_version}</owl:versionInfo>
    </owl:Ontology>\n\n'''


def model_annotation_properties(ontology):
    """ Model annotation properties from an Ontology object as an OWL RDF/XML string.

    Args:
        ontology (Ontology): Ontology object

    Returns:
        Modelled annotation properties OWL RDF/XML string

    """

    # Generate the annotation properties OWL RDF/XML string.
    modelled_annotation_properties = f'''
    <!-- ANNOTATION PROPERTIES -->\n\n
    <owl:AnnotationProperty rdf:about="http://www.w3.org/2004/02/skos/core#definition"/>\n\n'''
    for annotation_property in ontology.annotation_properties:
        modelled_annotation_properties += f'''
    <owl:AnnotationProperty rdf:about="{ontology.iri}#{annotation_property.id}">
        <rdfs:label xml:lang="en" {RDF_DATATYPE_STRING}>{annotation_property.name}</rdfs:label>
        <skos:definition xml:lang="en" {RDF_DATATYPE_STRING}>{annotation_property.description}</skos:definition>
    </owl:AnnotationProperty>\n\n'''
    return modelled_annotation_properties


def model_object_properties(ontology):
    """ Model object properties from an Ontology object as an OWL RDF/XML string.

    Args:
        ontology (Ontology): Ontology object

    Returns:
        Modelled object properties OWL RDF/XML string

    """

    # Generate the object properties OWL RDF/XML string.
    modelled_object_properties = f'''
    <!-- OBJECT PROPERTIES -->\n\n'''
    for object_property in ontology.object_properties:
        modelled_object_properties += f'''
    <owl:ObjectProperty rdf:about="{ontology.iri}#{object_property.id}">
        <rdfs:subPropertyOf {OWL_TOP_OBJECT_PROPERTY_IRI}/>
        <rdfs:label xml:lang="en" {RDF_DATATYPE_STRING}>{object_property.name}</rdfs:label>
    </owl:ObjectProperty>\n\n'''
    return modelled_object_properties


def model_class_things(ontology):
    """ Model thing classes from an Ontology object as an OWL RDF/XML string.

    Args:
        ontology (Ontology): Ontology object

    Returns:
        Modelled thing classes OWL RDF/XML string

    """

    # Generate the thing classes OWL RDF/XML string.
    modelled_class_things = f'''
    <!-- CLASSES - THINGS -->\n\n'''
    for class_thing in ontology.class_things:
        modelled_class_things += f'''
    <owl:Class rdf:about="{ontology.iri}#{class_thing.id}">
        <rdfs:label {RDF_DATATYPE_STRING}>{class_thing.name}</rdfs:label>
        <rdfs:comment {RDF_DATATYPE_STRING}>{class_thing.description}</rdfs:comment>
    </owl:Class>\n\n'''
    return modelled_class_things


def model_class_disciplines(ontology):
    """ Model discipline classes from an Ontology object as an OWL RDF/XML string.

    Args:
        ontology (Ontology): Ontology object

    Returns:
        Modelled discipline classes OWL RDF/XML string

    """

    # Generate the discipline classes OWL RDF/XML string.
    modelled_class_disciplines = f'''
    <!-- CLASSES - DISCIPLINES -->\n\n'''
    for class_discipline in ontology.class_disciplines:
        modelled_class_disciplines += f'''
    <owl:Class rdf:about="{ontology.iri}#{class_discipline.id}">
        <rdfs:subClassOf rdf:resource="{ontology.iri}#{class_discipline.thing_id}"/>
        <rdfs:subClassOf>
            <owl:Restriction>
                <owl:onProperty rdf:resource="{ontology.iri}#{class_discipline.object_property_id}"/>
                <owl:someValuesFrom rdf:resource="{ontology.iri}#{class_discipline.thing_id}"/>
            </owl:Restriction>
        </rdfs:subClassOf>
        <entityType xml:lang="en" {RDF_DATATYPE_STRING}>{ENTITY_TYPE_DISCIPLINE}</entityType>
        <rdfs:label {RDF_DATATYPE_STRING}>{class_discipline.name}</rdfs:label>
        <skos:definition xml:lang="en" {RDF_DATATYPE_STRING}>{class_discipline.description}</skos:definition>
    </owl:Class>\n\n'''
    return modelled_class_disciplines


def model_class_branches(ontology):
    """ Model branch classes from an Ontology object as an OWL RDF/XML string.

    Args:
        ontology (Ontology): Ontology object

    Returns:
        Modelled branch classes OWL RDF/XML string

    """

    # Generate the branch classes OWL RDF/XML string.
    modelled_class_branches = f'''
    <!-- CLASSES - BRANCHES -->\n\n'''
    for class_branch in ontology.class_branches:

        # Branch description (nullable)
        skos_definition = \
            (f'\n        <skos:definition xml:lang="en" {RDF_DATATYPE_STRING}>{class_branch.description}'
             f'</skos:definition>') if hasattr(class_branch, 'description') else ''

        # Branch responsibilities (nullable)
        responsibilities = \
            (f'\n        <responsibilities xml:lang="en" {RDF_DATATYPE_STRING}>{class_branch.responsibilities}'
             f'</responsibilities>') if hasattr(class_branch, 'responsibilities') else ''

        modelled_class_branches += f'''
    <owl:Class rdf:about="{ontology.iri}#{class_branch.id}">
        <rdfs:subClassOf rdf:resource="{ontology.iri}#{class_branch.discipline_id}"/>
        <rdfs:subClassOf>
            <owl:Restriction>
                <owl:onProperty rdf:resource="{ontology.iri}#{class_branch.object_property_id}"/>
                <owl:someValuesFrom rdf:resource="{ontology.iri}#{class_branch.discipline_id}"/>
            </owl:Restriction>
        </rdfs:subClassOf>
        <entityType xml:lang="en" {RDF_DATATYPE_STRING}>{ENTITY_TYPE_BRANCH}</entityType>
        <rdfs:label {RDF_DATATYPE_STRING}>{class_branch.name}</rdfs:label>{skos_definition}{responsibilities}
        <url xml:lang="en" rdf:resource="{class_branch.url}"/>
    </owl:Class>\n\n'''
    return modelled_class_branches


def model_class_skills(ontology, ddat_base_url, ddat_skills_resource):
    """ Model skill classes from an Ontology object as an OWL RDF/XML string.

    Args:
        ontology (Ontology): Ontology object
        ddat_base_url (string): Base URL to the DDaT profession capability framework website.
        ddat_skills_resource (string): Relative URL to the DDaT skills resource.

    Returns:
        Modelled skill classes OWL RDF/XML string

    """

    # Generate the skill classes OWL RDF/XML string.
    modelled_class_skills = f'''
    <!-- CLASSES - SKILLS -->\n\n'''
    for class_skill in ontology.class_skills:

        # Class attributes.
        class_iri = f'{ontology.iri}#{OWL_SKILL_CLASS_ID}{string_utils.pascal_case(class_skill.name)}'
        skill_url = f'{ddat_base_url}/{ddat_skills_resource}#{class_skill.anchor_id}'
        skill_iri = f'{ontology.iri}#{OWL_SKILL_CLASS_ID}'
        awareness_level_capabilities = model_skill_level_capabilities(class_skill.skill_levels['Awareness'])
        working_level_capabilities = model_skill_level_capabilities(class_skill.skill_levels['Working'])
        practitioner_level_capabilities = model_skill_level_capabilities(class_skill.skill_levels['Practitioner'])
        expert_level_capabilities = model_skill_level_capabilities(class_skill.skill_levels['Expert'])

        modelled_class_skills += f'''
    <owl:Class rdf:about="{class_iri}">
        <rdfs:subClassOf rdf:resource="{skill_iri}"/>
        <rdfs:label xml:lang="en">{class_skill.name}</rdfs:label>
        <skos:definition xml:lang="en" {RDF_DATATYPE_STRING}>{class_skill.description}</skos:definition>
        <entityType xml:lang="en" {RDF_DATATYPE_STRING}>{ENTITY_TYPE_SKILL}</entityType>
        <url xml:lang="en" rdf:resource="{skill_url}"/>
        <awarenessLevelCapabilities xml:lang="en" {RDF_DATATYPE_STRING}>{awareness_level_capabilities}</awarenessLevelCapabilities>
        <workingLevelCapabilities xml:lang="en" {RDF_DATATYPE_STRING}>{working_level_capabilities}</workingLevelCapabilities>
        <practitionerLevelCapabilities xml:lang="en" {RDF_DATATYPE_STRING}>{practitioner_level_capabilities}</practitionerLevelCapabilities>
        <expertLevelCapabilities xml:lang="en" {RDF_DATATYPE_STRING}>{expert_level_capabilities}</expertLevelCapabilities>
    </owl:Class>\n\n'''
    return modelled_class_skills


def model_skill_level_capabilities(skill_level_capabilities):
    """ Model skill level capabilities.

    Args:
        skill_level_capabilities (list): List of capabilities at a skill level.

    Returns:
        String representation of the list of capabilities at a skill level.
    """

    modelled_skill_level_capabilities = ''
    counter = 1
    for skill_level_capability in skill_level_capabilities:
        modelled_skill_level_capability = \
            f'{counter}. {skill_level_capability[0].upper()}{skill_level_capability[1:]}. \n'
        modelled_skill_level_capabilities += modelled_skill_level_capability
        counter += 1
    return modelled_skill_level_capabilities


def write_ontology_to_file(modelled_ontology, base_working_dir):
    """ Write the modelled ontology OWL RDF/XML string to file.

    Args:
        modelled_ontology (string):  Modelled ontology OWL RDF/XML string.
        base_working_dir (string): Path to the base working directory.

    """

    with open(f'{base_working_dir}/{OUTPUT_FILE_PATH}', 'w') as f:
        f.write(f'{modelled_ontology}')
