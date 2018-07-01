#!/usr/bin/env python
""" A context manager to simulate functioning of Ballard Locks """

class Locke:
    
    def __init__(self, max_boats):
        self.max_boats = max_boats

    def __enter__(self):
        return self

    def move_boats_through(self, number_boats):
        if number_boats > self.max_boats:
            raise ValueError
        else:
            print('Stopping the pumps.')
            print('Opening the doors.')
            print('Closing the doors.')
            print('Restarting the pumps.')

    def __exit__(self, e_type, e_val, e_tb):
        if e_type is ValueError:
            print('Warning: Too many boats for the locke!')


### Test parameters
small_locke = Locke(5)
large_locke = Locke(10)
boats = 8

### Case 1: A lock with sufficient capacity can move boats without incident.
print('*Test 1* - Sufficient Capacity')
with large_locke as locke:
    locke.move_boats_through(boats)

### Case 2: Too many boats through a small locke will raise an exception
print('\n*Test 2* - Too many boats')
with small_locke as locke:
    locke.move_boats_through(boats)

