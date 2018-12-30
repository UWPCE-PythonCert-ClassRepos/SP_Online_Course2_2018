#!/usr/bin/env python3

"""
example of using __metaclass__ to impliment the singleton pattern
"""


class MangledSingleton(type):
    instance = None

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__call__(*args, **kwargs)
        return cls.instance

    def __new__(cls, clsname, bases, _dict):
        uppercase_attr = {}
        for name, val in _dict.items():
            if not name.startswith('__'):
                uppercase_attr[name.upper()] = val
                uppercase_attr[name.lower()] = val
                uppercase_attr[name*2] = val
            else:
                uppercase_attr[name] = val

        return super().__new__(cls, clsname, bases, uppercase_attr)


class MyClass(metaclass=MangledSingleton):
    x = 1


if __name__ == "__main__":
    object1 = MyClass()
    object2 = MyClass()

    print(id(object1))
    print(id(object2))

    assert id(object1) == id(object2)