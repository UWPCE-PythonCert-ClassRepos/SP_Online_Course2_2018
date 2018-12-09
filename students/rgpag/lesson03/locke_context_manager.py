class Locke(object):

    def __init__(self, boat_limit):
        self.boat_limit = boat_limit

    def __enter__(self):
        print('Stopping pumps.')
        print('Opening doors.')
        print('Closing doors.')
        print('Restarting pumps.')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Stopping pumps.')
        print('Opening doors.')
        print('Closing doors')
        print('Restarting pumps')

    def move_boats_through(self, boats):
        if boats > self.boat_limit:
            raise ValueError("Can't move {} boats! Max capacity is {} boats at a time."
                             .format(boats, self.boat_limit))
        print('Plenty of room to move {} boats!'.format(boats))


small_locke = Locke(5)
large_locke = Locke(10)
boats = 8


# Too many boats through a small locke will raise an exception
with small_locke as locke:
    locke.move_boats_through(boats)

# A lock with sufficient capacity can move boats without incident.
with large_locke as locke:
    locke.move_boats_through(boats)
