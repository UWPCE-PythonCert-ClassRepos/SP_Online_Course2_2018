#!/usr/bin/env python3
# Lesson 3, Locke context manager

class Locke:
    """
    Context manager class for a locke
    """
    def __init__(self, max_boats):
        self.max_boats = max_boats

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
        Moves a specified number of boats through the lock, raising error if two many boats
        :param boats: the number of boats to move through the locke
        """
        if (boats <= self.max_boats):
            print("\nMoving {} boats through.".format(boats))
        else:
            raise ValueError("Can not move {} boats, more than max of {}".format(boats, self.max_boats))

small_locke = Locke(5)
large_locke = Locke(10)
boats = 8

# Too many boats through a small locke will raise an exception
with small_locke as locke:
    locke.move_boats_through(boats)

# A lock with sufficient capacity can move boats without incident.
with large_locke as locke:
    locke.move_boats_through(boats)