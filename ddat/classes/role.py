""" DDaT Role class. """

import ddat.utils.string_utils as string_utils
import json


class Role:

    def __init__(self, name, branch_id, description, url, responsibilities, civil_service_job_grades):
        """
        Args:
            name (string): Role name.
            branch_id (string): Branch ID
            description (string): Role description.
            url (string): Role URL including anchor ID.
            responsibilities (list): List of role responsibilities.
            civil_service_job_grades (list): List of role civil service job grades.
        """

        self.name = name
        self.branch_id = branch_id
        self.description = description
        self.url = url
        self.responsibilities = responsibilities
        self.civil_service_job_grades = civil_service_job_grades
        self.iri_id = string_utils.camel_case(name)
        self.skills = None

    def set_skills(self, skills):
        self.skills = skills

    def __str__(self):
        """ Override the __str__() method to return the class name followed
        by the string representation of the object's namespace dictionary.
        """

        return type(self).__name__ + str(vars(self))

    def to_json(self):
        """ JSON serializer. """

        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
