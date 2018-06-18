# Ballard Locks context manager exercise


class Locke(object):
    """
    Creates Locke objects
    """

    def __init__(self, boat_capacity):
        self.boat_capacity = boat_capacity

    def __enter__(self):
        print('Preparing to allow entry into locke.\n')
        typical_operation()
        print('\nBoats entering locke.')

    def __exit__(self, *args):
        print('Preparing locke for exiting.\n')
        typical_operation()
        print('\nBoats exiting locke.')

    @staticmethod
    def typical_operation():
        op_text = """
        Stopping the pumps.
        Opening the doors.
        Closing the doors.
        Restarting the pumps.
        """
        print(op_text)

    def move_boats_through(boats):
        try:
            assert boats <= self.boat_capacity
            self.__enter__()
            self.__exit__()
        except AssertionError:
            print('Number of boats exceeds locke\'s capacity.')
