#!/usr/bin/env python3

"""
Lesson 3 Assignment: Context Manager
"""

class Locke():
    def __init__(self, capacity):
        self.capacity = capacity
        print(f"Locke with capacity of {capacity} created.")

    def __enter__(self):
        print("""\nEntering locke:
        Stopping the pumps.
        Opening the doors.
        Closing the doors.
        Restarting the pumps.""")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("""\nExiting locke:
        Stopping the pumps.
        Opening the doors.
        Closing the doors.
        Restarting the pumps.""")

    def move_boats_through(self, num_boats):
        if num_boats > self.capacity:
            raise ValueError("Too many boats to move.")
        print(f"\nMoving {boats} boats through.")


if __name__ == "__main__":
    small_locke = Locke(5)
    large_locke = Locke(10)
    boats = 8

    # Too many boats through a small locke will raise an exception
    try:
        with small_locke as locke:
            locke.move_boats_through(boats)
    except ValueError as e:
        print('\nERROR: ' + str(e))

    # A lock with sufficient capacity can move boats without incident.
    with large_locke as locke:
        locke.move_boats_through(boats)
