#!/usr/bin/env python3

#Natalie Rodriguez
#UW Python - Course 2
#July 10, 2018
#Lesson 3

from contextlib import contextmanager

def pumps(func):
    def wrapper(*args, **kwargs):
        print("\nStopping the pumps.")
        result = func(*args, **kwargs)
        print("Restarting the pumps.")
        return result

    return wrapper


def doors(func):
    def wrapper(*args, **kwargs):
        print("Opening the doors.")
        result = func(*args, **kwargs)
        print("Closing the doors.")
        return result

    return wrapper


class Locke:
    def __init__(self, size):
        self.size = size
        self.queue = 0

    def __enter__(self):
        self.locke_function_process(True)
        return self

    def __exit__(self, e_type, e_value, e_traceback):
        if e_type == ValueError:
            print(e_value)
        self.locke_function_process(False)
        if self.queue > 0:
            with Locke(self.size) as locke:
                locke.move_boats_through(self.queue)
        return True

    @pumps
    @doors
    def locke_function_process(self, entering=True):
        if entering:
            print("Boats are entering the locke.")
        else:
            print("Boats are exiting the locke.")

    def move_boats_through(self, num_boats):
        self.queue = max(0, num_boats - self.size)
        if self.queue > 0:
            raise ValueError(f"The number of boats trying to pass ({num_boats}) "
                             f"exceeds the locke capacity of ({self.size}). {self.queue} "
                             f"boat(s) must wait for the next passage cycle.")
        else:
            print(f"{num_boats} boat(s) are passing through the locke.")


if __name__ == "__main__":
    small_locke = Locke(5)
    large_locke = Locke(10)

    # Too many boats through a small locke will raise an exception
    for boats in range(1, 30, 2):
        print(f"\n\t ***Small locke, {boats} boat(s) moving through the locks:***")
        with small_locke as locke:
            locke.move_boats_through(boats)

        # A lock with sufficient capacity can move boats without incident.
        print(f"\n\t ***Large locke, {boats} boat(s) moving through the locks:***")
        with large_locke as locke:
            locke.move_boats_through(boats)