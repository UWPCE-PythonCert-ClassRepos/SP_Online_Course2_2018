#!/usr/bin/env python3
# Ian Letourneau
# 8/30/2018

import sys
from contextlib import contextmanager

class Locke:
    def __init__(self, size):
        self.size = size

    def __enter__(self):
        print("Entering...")
        print("Stopping the pumps.")
        print("Opening the doors.")
        print("Closing the doors.")
        print("Restarting the pumps.")
        print("")
        return self

    def __exit__(self, *args):
        print("Exiting...")
        print("Stopping the pumps.")
        print("Opening the doors.")
        print("Closing the doors.")
        print("Restarting the pumps.")
        print("")

    def move_boats_through(self, boats):
        if self.size < boats:
            raise Exception("Holy, too many boats my man.")


small_locke = Locke(5)
large_locke = Locke(10)
boats = 8

# A lock with sufficient capacity can move boats without incident.
with large_locke as locke:
    locke.move_boats_through(boats)

# Too many boats through a small locke will raise an exception
with small_locke as locke:
    locke.move_boats_through(boats)
