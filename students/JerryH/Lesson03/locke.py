#!/usr/bin/env python3

class Locke:

    def __init__(self, boats):
        self.boats = boats

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return None

    def move_boats_through(self, num_boats):
        if num_boats < self.boats:
            print('==There is sufficient capity==')
            print('Stopping the pumps.')
            print('Opening the doors.')
            print('Closing the doors.')
            print('Restarting the pumps.')
        else:
            raise Exception('Too many boats.  Not Allowed')


small_locke = Locke(5)
large_locke = Locke(10)
boats = 8

# Too many boats through a small locke will raise an exception
with small_locke as locke:
    locke.move_boats_through(boats)

# A lock with sufficient capacity can move boats without incident.
with large_locke as locke:
    locke.move_boats_through(boats)
