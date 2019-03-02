#!/usr/bin/env python3
class BoatError(Exception):
    """Locke too small to accomodate boats."""
    def __init__(self, boats):
        self.boats = boats

class Locke():
    """Class to model behavior of canal lockes."""

    def __init__(self, capacity):
        self.capacity = capacity

    def __str__(self):
        return "Locke({})".format(self.capacity)

    def __enter__(self):
        print("\nEntering {}".format(self))
        self.stop_pumps()
        self.open_doors()
        self.close_doors()
        self.start_pumps()
        return self

    def __exit__(self, type, value, traceback):
        print("\nExiting {}".format(self))
        self.stop_pumps()
        self.open_doors()
        self.close_doors()
        self.start_pumps()
        if type is BoatError:
            return True
        else:
            return False

    def start_pumps(self):
        print("Restarting the pumps.")

    def stop_pumps(self):
        print("Restarting the pumps.")

    def open_doors(self):
        print("Opening the doors.")

    def close_doors(self):
        print("Closing the doors.")

    def move_boats_through(self, boats):
        if boats > self.capacity:
            print('\nError: unable to move {} boats through Locke of size {}.'
                .format(boats, self.capacity))
            raise BoatError(boats)
        else:
            print('\nMoving {} boats through Locke({}).'.format(boats,
                self.capacity))

if __name__ == '__main__':
    small_locke = Locke(5)
    large_locke = Locke(10)
    boats = 8

    with large_locke as locke:
        locke.move_boats_through(boats)

    with small_locke as locke:
        locke.move_boats_through(boats)
