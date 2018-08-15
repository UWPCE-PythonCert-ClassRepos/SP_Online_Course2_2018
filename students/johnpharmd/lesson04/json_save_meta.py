#!/usr/bin/env python3

"""
json_save

USE THIS LINK FOR HELP: https://realpython.com/python-json/

metaclass based system for saving objects in a JSON format

This could be useful, but it's kept simple to show the use of metaclasses

The idea is that you subclass from JsonSaveable, and then you get an object
that be saved and reloaded to/from JSON
"""

import json
from saveables import *


class MetaJsonSaveable(type):
    """
    The metaclass for creating JsonSaveable classes

    Deriving from type makes it a metaclass.
    """

    # def __new__(type, name, bases, attr_dict):
    #     return super().__new__(type, name, bases, attr_dict)

    def __init__(cls, name, bases, attr_dict):
        """
        Note: the __init__ gets run at compile time, not run time.
        (module import time)
        """
        # it gets the class object as the first param.
        # and then the same parameters as the type() factory function

        # you want to call the regular type initilizer:
        print('Initializing class', cls)
        super(MetaJsonSaveable, cls).__init__(name, bases, attr_dict)

        # here's where we work with the class attributes:
        # these will be the attributes that get saved and reconstructed from json.
        # each class object gets its own dict
        cls._attrs_to_save = {}
        for key, attr in attr_dict.items():
            if isinstance(attr, Saveable):
                cls._attrs_to_save[key] = attr
        # special case JsonSaveable -- no attrs to save yet
        if cls.__name__ != "JsonSaveable" and (not cls._attrs_to_save):
            raise TypeError(f"{cls.__name__} class has no saveable attributes.\n"
                            "           Note that Saveable attributes must be instances")

        # register this class so we can re-construct instances.
        cls.ALL_SAVEABLES[attr_dict["__qualname__"]] = cls
        # cls.__new__(cls)


class JsonSaveable(metaclass=MetaJsonSaveable):
    """
    mixin for JsonSaveable objects
    """
    def __new__(cls, *args, **kwargs):
        """
        This adds instance attributes to assure they are all there, even if
        they are not set in the subclasses __init__
        """
        # create the instance
        obj = super().__new__(cls)
        # set the instance attributes to defaults
        for attr, typ in cls._attrs_to_save.items():
            setattr(obj, attr, typ.default)
        return obj

    def __eq__(self, other):
        """
        default equality method that checks if all of the saved attributes
        are equal
        """
        for attr in self._attrs_to_save:
            try:
                if getattr(self, attr) != getattr(other, attr):
                    return False
            except AttributeError:
                return False
        return True

    def to_json_compat(self, *args):
        """
        converts this object to a json-compatible dict.

        returns the dict
        """
        # add an __obj_type attribute, so it can be reconstructed
        dic = {"__obj_type": self.__class__.__qualname__}
        for attr, typ in self._attrs_to_save.items():
            dic[attr] = typ.to_json_compat(getattr(self, attr))
        return dic

    @classmethod
    def from_json_dict(cls, dic):
        """
        creates an instance of this class populated by the contents of
        the json compatible dict

        the object is created with __new__ before setting the attributes

        NOTE: __init__ is not called.
        There should not be any extra initialization required in __init__
        """
        # create a new object
        obj = cls.__new__(cls)
        for attr, typ in cls._attrs_to_save.items():
            setattr(obj, attr, typ.to_python(dic[attr]))
        # make sure it gets initialized
        obj.__init__()
        return obj

    def to_json(self, fp=None, indent=4):
        """
        Converts the object to JSON

        :param fp=None: an open file_like object to write the json to.
                        If it is None, then a string with the JSON
                        will be returned as a string

        :param indent=4: The indentation level desired in the JSON
        """
        if fp is None:
            return json.dumps(self.to_json_compat(), indent=indent)
        else:
            json.dump(self.to_json_compat(), fp, indent=indent)

    def __str__(self):
        msg = ["{} object, with attributes:".format(self.__class__.__qualname__)]
        for attr in self._attrs_to_save.keys():
            msg.append("{}: {}".format(attr, getattr(self, attr)))
        return "\n".join(msg)


def from_json_dict(j_dict):
    """
    factory function that creates an arbitrary JsonSaveable
    object from a json-compatible dict.
    """
    # determine the class it is.
    obj_type = j_dict["__obj_type"]
    obj = Saveable.ALL_SAVEABLES[obj_type].from_json_dict(j_dict)
    return obj


def from_json(_json):
    """
    factory function that re-creates a JsonSaveable object
    from a json string or file
    """
    if isinstance(_json, str):
        return from_json_dict(json.loads(_json))
    else:  # assume a file-like object
        return from_json_dict(json.load(_json))


if __name__ == "__main__":

    # Example of using it.
    class MyClass(JsonSaveable):

        x = 1
        y = 1.0
        l = []

        def __init__(self, x, lst):
            self.x = x
            self.lst = lst
            self.attr_dict = {'x': self.x, 'lst': self.lst}

    class OtherSaveable(JsonSaveable):

        # foo = str(foo)
        # bar = int(bar)

        def __init__(self, foo, bar):
            self.foo = foo
            self.bar = bar
            self.attr_dict = {'foo': self.foo, 'bar': self.bar}

    # create one:
    print("about to create an instance of MyClass (p-statement01; line 185)")
    mc = MyClass(5, [3, 5, 7, 9])

    print('p-statement02:', mc)

    jc = mc.to_json_compat()

    # re-create it from the dict:
    mc2 = MyClass.from_json_dict(jc)

    print('p-statement03:', mc2 == "fred")

    print('Assertion: mc2 == mc')
    assert mc2 == mc

    print('p-statement04:', mc.to_json())

    # now try it nested...
    mc_nest = MyClass(34, [OtherSaveable("this", 2),
                           OtherSaveable("that", 64),
                           ])

    mc_nest_comp = mc_nest.to_json_compat()
    print('p-statement05:', mc_nest_comp)

    # can we re-create it?
    mc_nest2 = MyClass.from_json_dict(mc_nest_comp)

    print('p-statement06:', mc_nest)
    print('p-statement07:', mc_nest2)

    assert mc_nest == mc_nest2
