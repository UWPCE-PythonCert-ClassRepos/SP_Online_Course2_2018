#!/usr/bin/env python3


class Locke:

    def __init__(self, limit):
        self._limit = limit
        self._boats = None

    def __enter__(self):
        print("{} activated.".format(self.size))
        print("Stopping the pumps.")
        return self

    def __exit__(self, e_type, e_val, e_traceback):
        print("Restarting the pumps.")
        print("{} deactivated.".format(self.size))
        return False

    @property
    def limit(self):
        return self._limit

    @property
    def boats(self):
        return self._boats

    @boats.setter
    def boats(self, val):
        if not val:
            raise ValueError("Locke must receive number of boats entering.")
        self._boats = val

    @property
    def size(self):
        return "SMALL LOCKE" if self.limit <= 5 else "LARGE LOCKE"

    def open_doors(self):
        print("Opening the doors.")

    def close_doors(self):
        print("Closing the doors.")

    def check_entry_conditions(self):
        if not self.boats <= self.limit:
            raise ValueError
        return True

    def move_boats_through(self, num_boats):
        self.boats = num_boats
        try:
            self.check_entry_conditions()
        except ValueError:
            raise ValueError("{} accepts {} boats max."
                             .format(self.size, self.limit))
        else:
            self.open_doors()
            self.close_doors()
