#!/usr/bin/env python

class Locke(object):

    def __init__(self, capacity):
        self.capacity = capacity

    def __enter__(self):
        print("Entering...")
        print("Stoping the pumps")
        print("Opening the doors")
        print("Closing the doors")
        print("Restarting the pumps")
        return self
       
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is ValueError:
            print("{}: {} {}".format(exc_type, exc_val, exc_tb))
        print("Exiting...")
        print("Stoping the pumps")
        print("Opening the doors")
        print("Closing the doors")
        print("Restarting the pumps")
        return True

    def move_boats_through(self, boats):
        if boats <= self.capacity:
            print("The number of boats meets the given capacity. Moving boats through")
        else:
            raise ValueError("The number of boats exceeds this locke's capacity")


small_locke = Locke(5)
large_locke = Locke(10)
boats = 8


if __name__ == "__main__":
    # Too many boats through a small locke will raise an exception
    print("Too many boats through a small locke will raise an exception")
    with small_locke as locke:
        locke.move_boats_through(boats)

    #A lock with sufficient capacity can move boats without incident.
    print("A lock with sufficient capacity can move boats without incident.")
    with large_locke as locke:
        locke.move_boats_through(boats)

    # Too many boats through a large locke will raise an exception
    print("Too many boats through a large locke will raise an exception")
    with large_locke as locke:
        locke.move_boats_through(11)

    #A lock with sufficient capacity can move boats without incident.
    print("A lock with sufficient capacity can move boats without incident.")
    with small_locke as locke:
        locke.move_boats_through(3)










