#!/usr/bin/env python3

class Locke:
    """
    A simple Locke context manager
    """
    def __init__(self, capacity):
        self.capacity = capacity

    def __enter__(self):
        print("\nStopping the pumps.")
        print("Opening the doors.")
        print("Closing the doors.")
        print("Restarting the pumps.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is ValueError:
            print(f"Error: {exc_val}")
        print("\nStopping the pumps.")
        print("Opening the doors.")
        print("Closing the doors.")
        print("Restarting the pumps.")
        return True

    def move_boats_through(self, boats):
        """
        Move the given number of boats through locke unless the number exceeds capacity
        :param boats: the number of boats to move through the locke
        """
        if (boats <= self.capacity):
            print(f"\nMoving {boats} boats through.")
        else:
            raise ValueError("Too many boats!")

small_locke = Locke(5)
large_locke = Locke(10)
boats = 8

# Too many boats through a small locke will raise an exception
with small_locke as locke:
    locke.move_boats_through(boats)

# A lock with sufficient capacity can move boats without incident.
with large_locke as locke:
    locke.move_boats_through(boats)