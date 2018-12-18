#!/usr/bin/env python3


class Locke(object):

    def __init__(self, boat_limit):
        self.capacity = boat_limit

    def __enter__(self):
        print("Stopping the pumps.")
        self.pumps_on = False
        print("Opening the doors")
        self.door_closed = False
        return self

    def move_boats_through(self, boats):
        if boats > self.capacity:
            raise ValueError("boats passing through doors "
                             "exceeds Locke capacity")

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing the doors")
        self.door_closed = True
        print("Restarting the pumps")
        self.pumps_on = True
        if (exc_type, exc_val, exc_tb) != (None, None, None):
            print('__exit__({}, {}, {})'.format(exc_type, exc_val, exc_tb))
