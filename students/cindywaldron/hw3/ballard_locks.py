#!/usr/bin/env python3

class Locke:
    def __init__(self, boats):
        self.boats = boats

    def __enter__(self):
        print("Stopping the pumps")
        print("Opening the doors")
        print("Closing the doors")
        print("Restarting the pumps")
        return self

    def __exit__(self, type, value, traceback):
        if type is not None:
            print(value)
        print("Stopping the pumps")
        print("Opening the doors")
        print("Closing the doors")
        print("Restarting the pumps")
        return True

    def move_boats_through(self, numOfBoats):
        if self.boats < numOfBoats:
            raise Exception("Maximum capacity exceeded.")
        else:
            print("Moving boats through")

if __name__ == "__main__":
    small_locke = Locke(5)
    large_locke = Locke(10)
    boats = 8

    with small_locke as locke:
        locke.move_boats_through(boats)

    with large_locke as locke:
        locke.move_boats_through(boats)