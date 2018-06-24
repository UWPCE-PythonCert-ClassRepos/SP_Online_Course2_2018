# Ballard Locks context manager exercise
from time import sleep


class Locke(object):
    """
    Creates Locke objects
    """

    def __init__(self, boat_capacity):
        self.boat_capacity = boat_capacity

    def typical_operation(*args):
        op_text = """
        Stopping the pumps.
        Opening the doors.
        Closing the doors.
        Restarting the pumps.
        """
        sleep(2)
        print(op_text)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        print('\nLocke operation halted.')

    def move_boats_through(self, boats):
        try:
            assert boats <= self.boat_capacity
            print('Preparing to allow entry into locke.\n')
            self.typical_operation()
            print('\nBoats entering locke.')
            print('Preparing locke for exiting.\n')
            self.typical_operation()
            print('\nBoats have exited locke.')
        except AssertionError:
            print('Number of boats exceeds locke\'s capacity.')
