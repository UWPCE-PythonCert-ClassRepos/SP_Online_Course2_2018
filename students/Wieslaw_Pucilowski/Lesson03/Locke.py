#!/usr/bin/env python3
__author__ = "Wieslaw Pucilowski"

class Locke:
    def __init__(self, size):
        self.size = size
        self.boats = 0

    def __enter__(self):
        print("Stopping the pumps.")
        print("Opening the doors.")
        return self

    def move_boats_through(self, boats):
        self.boats = boats
        if self.boats > self.size:
            raise ValueError("Number of boats: {} exceeds lock size {}"
                             .format(self.boats,self.size))
        else:
            print("Moving {} boats through the Locke..."
                  .format(self.boats))

    def __exit__(self, exc_type, exc_val, exc_trace):
        if exc_type:    # if exception
            print("Attention: {}".format(exc_val))
            print("Please try with reduced boats number....")
        else:
            print("Closing the doors.")
            print("Restarting the pumps")
        return True


if __name__ == '__main__':
    small_locke = Locke(5)
    large_locke = Locke(10)
    boats = 8

    print("\nTest for {} boats going through large lock {}\n"
          .format(boats, large_locke.size))
    with large_locke as locke:
        locke.move_boats_through(boats)
    print("\nTest for {} boats going through small lock {}\n"
          .format(boats, small_locke.size))
    with small_locke as locke:
        locke.move_boats_through(boats)
