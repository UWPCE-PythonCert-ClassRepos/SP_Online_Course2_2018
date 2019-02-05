#!/usr/bin/env python3

"""
Lesson 3 Assignment: Context Manager
"""

class Locke():
    def __init__(self, capacity):
        self.capacity = capacity
        print(f"\nLocke with capacity of {capacity} created.")

    def __enter__(self):
        print("""\nEntering locke:
        Stopping the pumps.
        Opening the doors.
        Closing the doors.
        Restarting the pumps.""")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"\nERROR: {exc_val}")
        print("""\nExiting locke:
        Stopping the pumps.
        Opening the doors.
        Closing the doors.
        Restarting the pumps.""")
        return True

    def move_boats_through(self, num_boats):
        if num_boats > self.capacity:
            raise ValueError("Too many boats to move.")
        print(f"\nMoving {boats} boats through.")


if __name__ == "__main__":

    # Too many boats through a small locke will raise an exception
    small_locke = Locke(5)
    boats = 3
    with small_locke as locke:
        locke.move_boats_through(boats)

    boats = 8
    with small_locke as locke:
        locke.move_boats_through(boats)

    # A lock with sufficient capacity can move boats without incident.
    large_locke = Locke(10)
    boats = 8
    with large_locke as locke:
        locke.move_boats_through(boats)
