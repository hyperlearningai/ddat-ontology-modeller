""" DDaT Ontology class. """

import json


class Ontology:

    def __init__(self, name, iri, description, owl_version, contributors):
        """
        Args:
            name (string): Ontology name
            iri (string): Ontology IRI
            description (string): Ontology description
            owl_version (string): Ontology OWL version
            contributors (list): List of ontology contributors
        """

        self.name = name
        self.iri = iri
        self.description = description
        self.owl_version = owl_version
        self.contributors = contributors
        self.annotation_properties = None
        self.object_properties = None
        self.class_things = None
        self.class_disciplines = None
        self.class_branches = None
        self.class_skills = None
        self.class_roles = None

    def set_annotation_properties(self, annotation_properties):
        self.annotation_properties = annotation_properties

    def set_object_properties(self, object_properties):
        self.object_properties = object_properties

    def set_class_things(self, class_things):
        self.class_things = class_things

    def set_class_disciplines(self, class_disciplines):
        self.class_disciplines = class_disciplines

    def set_class_branches(self, class_branches):
        self.class_branches = class_branches

    def set_class_skills(self, class_skills):
        self.class_skills = class_skills

    def set_class_roles(self, class_roles):
        self.class_roles = class_roles

    def __str__(self):
        """ Override the __str__() method to return the class name followed
        by the string representation of the object's namespace dictionary.
        """

        return type(self).__name__ + str(vars(self))

    def to_json(self):
        """ JSON serializer. """

        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
