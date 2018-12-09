#!/usr/bin/env python3


class Locke:

    """
    Write a context manager class Locke to simulate the overall functioning of the system. When the locke is entered it
    stops the pumps, opens the doors, closes the doors, and restarts the pumps. Likewise when the locke is exited it
    runs through the same steps: it stops the pumps, opens the doors, closes the doors, and restarts the pumps.
    Don’t worry for now that in the real world there are both upstream and downstream doors, and that they should never
    be opened at the same time; perhaps you’ll get to that later. During initialization the context manager class
    accepts the locke’s capacity in number of boats. If someone tries to move too many boats through the locke,
    anything over its established capacity, raise a suitable error. Since this is a simulation you need do nothing
    more than print what is happening with the doors and pumps.
    """

    def __init__(self, boats):
        self.boats = boats
        self.exception = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.exception:
            print('__exit__({}, {}, {})'.format(exc_type, exc_val, exc_tb))
        else:
            pass
        return self.exception

    def move_boats_through(self, num_of_boats):
        if num_of_boats < self.boats:
            print('Stopping the pumps.')
            print('Opening the doors.')
            print('Closing the doors.')
            print('Restarting the pumps.')
        else:
            self.exception = True
            raise Exception("Number of boats exceeds locke capacity")


small_locke = Locke(5)
large_locke = Locke(10)
boats = 6

# Too many boats through a small locke will raise an exception
with small_locke as locke:
    locke.move_boats_through(boats)

print()
# A lock with sufficient capacity can move boats without incident.
with large_locke as locke:
    locke.move_boats_through(boats)
