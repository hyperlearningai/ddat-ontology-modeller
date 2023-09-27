""" Ontology modeller pipeline module. """

import json

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

# Output file relative path and name.
OUTPUT_FILE_PATH = 'modelled/ddat.owl'

# OWL RDF/XML substrings.
RDF_DATATYPE_STRING = 'rdf:datatype="http://www.w3.org/2001/XMLSchema#string"'


def run(model_dir_path, base_working_dir):
    """ Run this pipeline module.

    Args:
        model_dir_path (string): Path to the directory holding the ontology model.
        base_working_dir (string): Path to the base working directory.

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

    # Model the Ontology as an OWL RDF/XML ontology.
    modelled_ontology = model_ontology(ontology)

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


def model_ontology(ontology):
    """ Model an Ontology object as an OWL RDF/XML ontology.

    Args:
        ontology (Ontology): Ontology object

    Returns:
        Modelled ontology OWL RDF/XML string

    """

    return f'''
<?xml version="1.0"?>
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
    xmlns:terms="http://purl.org/dc/terms/">
    <owl:Ontology rdf:about="{ontology.iri}">
        <dc:title xml:lang="en">{ontology.name}</dc:title>
        <rdfs:label xml:lang="en" {RDF_DATATYPE_STRING}>{ontology.name}</rdfs:label>
        <terms:contributor>Jillur Quddus</terms:contributor>
        <dc:description xml:lang="en">{ontology.description}</dc:description>
        <owl:versionInfo {RDF_DATATYPE_STRING}>{ontology.owl_version}</owl:versionInfo>
    </owl:Ontology>
    <owl:AnnotationProperty rdf:about="http://www.w3.org/2004/02/skos/core#definition"/>'''


def write_ontology_to_file(modelled_ontology, base_working_dir):
    """ Write the modelled ontology OWL RDF/XML string to file.

    Args:
        modelled_ontology (string):  Modelled ontology OWL RDF/XML string.
        base_working_dir (string): Path to the base working directory.

    """

    with open(f'{base_working_dir}/{OUTPUT_FILE_PATH}', 'w') as f:
        f.write(f'{modelled_ontology}')
