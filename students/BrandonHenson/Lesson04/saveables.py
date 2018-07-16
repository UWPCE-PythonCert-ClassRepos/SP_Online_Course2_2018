#!/usr/bin/env python

"""
The Saveable objects used by both the metaclass and decorator approach.
"""
import ast

# import json

__all__ = ['Bool',
           'Dict',
           'Float',
           'Int',
           'List',
           'Saveable',
           'String',
           'Tuple',
           ]


class Saveable():
    """
    Base class for all saveable types
    """
    default = None
    ALL_SAVEABLES = {}

    @staticmethod
    def to_json_compat(val):
        """
        returns a json-compatible version of val

        should be overridden in saveable types that are not json compatible.
        """
        return val

    @staticmethod
    def to_python(val):
        """
        convert from a json compatible version to the python version

        Must be overridden if not a one-to-one match

        This is where validation could be added as well.
        """
        return val


class String(Saveable):
    """
    A Saveable string

    Strings are the same in JSON as Python, so nothing to do here
    """
    default = ""


    @staticmethod
    def to_python(val):
        """
        Convert a number to a python integer
        """
        return int(val)





class List(Saveable):
    """
    This assumes that whatever is in the list is Saveable or a "usual"
    type: numbers, strings.
    """
    default = []

    @staticmethod
    def to_json_compat(val):
        lst = []
        for item in val:
            try:
                lst.append(item.to_json_compat())
            except AttributeError:
                lst.append(item)
        return lst

    @staticmethod
    def to_python(val):
        """
        Convert an array to a list.

        Complicated because list may contain non-json-compatible objects
        """
        # try to reconstitute using the obj method
        new_list = []
        for item in val:
            try:
                obj_type = item["__obj_type"]
                obj = Saveable.ALL_SAVEABLES[obj_type].from_json_dict(item)
                new_list.append(obj)
            except (TypeError, KeyError):
                new_list.append(item)
        return new_list



    @staticmethod
    def to_python(val):
        """
        Convert a json object to a dict

        Complicated because object may contain non-json-compatible objects
        """

        # try to reconstitute using the obj method
        new_dict = {}
        key_not_string = val.pop('__key_not_string', False)
        for key, item in val.items():
            if key_not_string:
                key = ast.literal_eval(key)
            try:
                obj_type = item["__obj_type"]
                obj = Saveable.ALL_SAVEABLES[obj_type].from_json_dict(item)
                new_dict[key] = obj
            except (KeyError, TypeError):
                new_dict[key] = item
        return new_dict
