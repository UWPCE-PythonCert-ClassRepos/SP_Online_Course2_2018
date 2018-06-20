#!/usr/bin/env python3


class Locke:

    def __init__(self, limit):
        self._limit = limit

    def __enter__(self):
        print("Stopping the pumps.")
        return self

    def __exit__(self, e_type, e_val, e_traceback):
        print("Restarting the pumps.")
        return False

    @property
    def limit(self):
        return self._limit

    @limit.setter
    def limit(self, val):
        if not val:
            raise ValueError("Locke must have a boat limit.")
        self._limit = val

    def move_boats_through(num_boats):
        pass
