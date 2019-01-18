#!/usr/bin/env python3

from contextlib import contextmanager
from contextlib import ContextDecorator
import pytest


class Locke():

    def __init__(self, locke_capacity):
        self.locke_capacity = locke_capacity

    @property
    def locke_capacity(self):
        return self._locke_capacity

    @locke_capacity.setter
    def locke_capacity(self, locke_capacity):
        if locke_capacity <= 0:
            raise ValueError("Capacity must be greater than 0.")
        else:
            self._locke_capacity = locke_capacity

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is ValueError:
            print("Too many boats.")
            print(exc_val)

    def prep_locks(func):
        def inner_func(*args, **kwargs):
            print("Stop pumps.")
            print("Opening doors.")
            result = func(*args, **kwargs)
            print("Closing doors.")
            print("Restarting pumps.")
            return result

        return inner_func

    @prep_locks
    def move_boats_through(self, boats):
        if boats < 0:
            raise ValueError("Wait for boats.")
        elif boats == 0:
            print("Testing the locke.")
        else:
            if boats > self.locke_capacity:
                raise ValueError("Reached maximum boat capacity for this locke. Wait for the next round.")
            else:
                print("The boats have sailed through.")


if __name__ == "__main__":
    small_locke = Locke(5)
    large_locke = Locke(10)
    max_locke = Locke(8)
    boats_to_sail = 8
    no_boats = 0

    '''print("Small locke can't fit too many boat. Boats need to wait for the next round.")
    with small_locke as locke:
        locke.move_boats_through(boats_to_sail)'''

    print("------------------------")

    print("Large locke to manage the serviced boats.")
    with large_locke as locke:
        locke.move_boats_through(boats_to_sail)

    print("------------------------")

    print("Locke used at maximum")
    with max_locke as locke:
        locke.move_boats_through(boats_to_sail)

    print("------------------------")

    print("No boats:")
    with large_locke as locke:
        locke.move_boats_through(no_boats)
