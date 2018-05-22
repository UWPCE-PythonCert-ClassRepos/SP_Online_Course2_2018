#!/usr/bin/env python3


class Locke:

    def __init__(self, boats):
        self.boats = boats

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return None

    def move_boats_through(self, no_of_boats):
        if no_of_boats > self.boats:
            raise Exception('Too many boats')
        else:
            print("Stopping the pumps.")
            print("Opening the doors.")
            print("Closing the doors.")
            print("Restarting the pumps.")


if __name__ == '__main__':
    small_locke = Locke(5)
    large_locke = Locke(10)
    boats = 8

    # A lock with sufficient capacity can move boats without incident.
    with large_locke as locke1:
        locke1.move_boats_through(boats)

    # Too many boats through a small locke will raise an exception
    with small_locke as locke2:
        locke2.move_boats_through(boats)
