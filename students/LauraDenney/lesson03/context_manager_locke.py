#-------------------------------------------------#
# Title: Context Managers: Lockes
# Dev:   LDenney
# Date:  February 11th, 2019
# ChangeLog: (Who, When, What)
#   Laura Denney, 2/11/19, Started work on context Managers Assignment
#   Laura Denney, 2/13/19, Finished testing
#-------------------------------------------------#

from contextlib import contextmanager

class Locke(object):

    def __init__(self,boat_capacity):
        self.boat_capacity=boat_capacity

    def __repr__(self):
        return "Locke capacity is {} boats.".format(self.boat_capacity)

    def __enter__(self):
        self.pump = "stop"
        print("Stopping the pumps.")
        self.door = "open"
        print("Opening the doors.")
        self.door = "close"
        print("Closing the doors.")
        self.pump = "start"
        print("Restarting the pumps.")
        return self


    def __exit__(self,exc_type, exc_val, exc_tb):
        if exc_type:
            print("{}".format(exc_val))
        self.pump = "stop"
        print("Stopping the pumps.")
        self.door = "open"
        print("Opening the doors.")
        self.door = "close"
        print("Closing the doors.")
        self.pump = "start"
        print("Restarting the pumps.\n")

    def move_boats_through(self, boats):
        if boats <= self.boat_capacity:
            print("Boats moving through the lockes.")
        else:
            raise ValueError("Too many boats, will not fit in lockes.")

def locke_spectator(locke, boats):
    print(locke)
    print(f"Number of boats attempting passage: {boats}")
    with locke as spectacle:
        try:
            spectacle.move_boats_through(boats)
        except ValueError as e:
            print(e)

if __name__ == "__main__":
    small_locke = Locke(4)
    large_locke = Locke(8)

    locke_spectator(small_locke, 3)
    locke_spectator(small_locke, 5)
    locke_spectator(large_locke, 6)
    locke_spectator(large_locke, 9)
