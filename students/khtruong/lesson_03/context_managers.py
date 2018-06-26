#!/usr/bin/env python


class Locke(object):

    def __init__(self, capacity):
        self._cap = capacity
        self._error = False

    def __enter__(self):
        print('Stopping the pumps.')
        print('Opening the doors.')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._error:
            print('__exit__({}, {}, {})'.format(exc_type, exc_val, exc_tb))
        else:
            print('Closing the doors.')
            print('Restarting the pumps.')
        return self._error

    def move_boats_through(self, boats):
        if boats > self._cap:
            self._error = True
            raise ValueError('Over Capacity!')

if __name__ == "__main__":
    small_locke = Locke(5)
    large_locke = Locke(10)
    boats = 8

    print('Small Locke - Raise Exception')
    print('-----------------------------')
    # Too many boats through a small locke will raise an exception
    with small_locke as locke:
        locke.move_boats_through(boats)
    print()
    print('Large Locke - Gucci!')
    print('--------------------')
    # A lock with sufficient capacity can move boats without incident.
    with large_locke as locke:
        locke.move_boats_through(boats)
