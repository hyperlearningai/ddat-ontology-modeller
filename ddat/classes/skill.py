#!/usr/bin/env python3
""" DDaT Skill. """

import ddat.utils.string_utils as string_utils
import json


class Skill:
    
    def __init__(self, anchor_id, name, description, skill_levels):
        """
            Args:
                anchor_id (string): Skill web element anchor ID.
                name (string): Skill name.
                description (string): Skill description.
                skill_levels (dict): Dictionary of capabilities at different skill levels.
        """

        self.anchor_id = anchor_id
        self.name = name
        self.description = description
        self.skill_levels = skill_levels
        self.id = string_utils.camel_case(name)

    def __str__(self):
        """ Override the __str__() method to return the class name followed
        by the string representation of the object's namespace dictionary.
        """
        
        return type(self).__name__ + str(vars(self))

    def to_json(self):
        """ JSON serializer. """

        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
