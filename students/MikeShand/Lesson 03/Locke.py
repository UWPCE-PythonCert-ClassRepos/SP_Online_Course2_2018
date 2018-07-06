#!/usr/bin/env python3

class Locke:
    def __init__(self, size):
        self.size = size

    def __enter__(self):
        print("Stopping the pumps.")
        print("Opening the doors.")
        return self

    def move_boats_through(self, boats):
        self.boats = boats
        if self.boats > self.size:
            raise ValueError(f'Number of boats({self.boats}) exceeds lock size({self.size})')
        else:
            print(f'Moving {self.boats} boats through!')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            print("Closing the doors.")
            print("Restarting the pumps")
        else:
            print("Please try again with fewer boats")


if __name__ == '__main__':
    small_locke = Locke(5)
    large_locke = Locke(10)
    boats = 8

    # Too many boats through a small locke will raise an exception
    with small_locke as locke:
        locke.move_boats_through(boats)

    # A lock with sufficient capacity can move boats without incident.
    # with large_locke as locke:
    #   locke.move_boats_through(boats)