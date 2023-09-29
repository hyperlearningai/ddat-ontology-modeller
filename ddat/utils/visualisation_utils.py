""" DDaT ontology visualisation utility functions. """

# Filter windows.
CLASS_THING_SKILL_LINE_COUNT = 5


def filter_ontology(skill_iri, modelled_ddat_ontology_owl_file_path, filtered_ddat_ontology_owl_file_path):
    """ Filter a post-modelled DDaT ontology OWL RDF/XML file for visualisation
    by removing the Skill parent class and relationships to it thereby
    removing links that do not add value to the ontology visualisation.

    Args:
        skill_iri (string): Skill class IRI.
        modelled_ddat_ontology_owl_file_path (string): Path to the post-modelled DDaT ontology OWL file.
        filtered_ddat_ontology_owl_file_path (string): Path to which to save the filtered DDaT ontology OWL file.

    """

    # Class and subclass relationships to remove from the ontology
    skill_owl_class_line_number_start = None
    skill_owl_class_line_number_end = None
    skill_owl_class_to_filter = f'<owl:Class rdf:about="{skill_iri}">'
    skill_rdfs_subclass_to_filter = f'<rdfs:subClassOf rdf:resource="{skill_iri}"/>'

    # Open and read the post-modelled DDaT ontology OWL file
    with open(modelled_ddat_ontology_owl_file_path, 'r') as f:
        modelled_ddat_ontology_lines = f.readlines()

    # Open and write to the filtered DDaT ontology OWL file
    with (open(filtered_ddat_ontology_owl_file_path, 'w') as f):
        counter = -1
        for modelled_ddat_ontology_line in modelled_ddat_ontology_lines:
            counter += 1

            # Identify the line numbers containing the skill class to filter
            if skill_owl_class_to_filter in modelled_ddat_ontology_line:
                skill_owl_class_line_number_start = counter
                skill_owl_class_line_number_end = counter + CLASS_THING_SKILL_LINE_COUNT
                continue

            # Filter out the skill class definition
            if (skill_owl_class_line_number_start is not None and
                    skill_owl_class_line_number_end is not None and
                    skill_owl_class_line_number_start <= counter <= skill_owl_class_line_number_end):
                continue

            # Filter out the subclass relationships to the skill class
            if skill_rdfs_subclass_to_filter not in modelled_ddat_ontology_line:
                f.write(modelled_ddat_ontology_line)
