#!/usr/bin/env python3


class Locke:

    def __init__(self, limit):
        self._limit = limit

    def __enter__(self):
        pass

    def __exit__(self, e_type, e_val, e_traceback):
        pass

    @property
    def limit(self):
        return self._limit

    @limit.setter
    def limit(self, val):
        if not val:
            raise ValueError("A Locke must have a boat limit.")
        self._limit = val
