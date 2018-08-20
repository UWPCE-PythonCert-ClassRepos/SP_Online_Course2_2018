#!/usr/bin/env python3

"""
Lesson3 - Context Mangers
"""


class Locke:
    def __init__(self, capacity):
        print('__init__({})'.format(capacity))
        self.capacity = capacity
        self.boats = 0

    def __enter__(self):
        print('__enter__()')
        print("Stopping the pumps.")
        print("Opening the doors.")
        print("Boats entering locke.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is ValueError:
            print(exc_val)
            return True
        print("Stopping the pumps.")
        print("Opening the doors.")
        print("Closing the doors.")
        print("Restarting the pumps.")
        print("Boats exited locke.")
        return self.boats

    def move_boats_through(self, boats):
        if self.capacity < boats:
            raise ValueError(f'{boats - self.capacity} too many boats')
        else:
            self.boats = boats
            print("Closing the doors.")
            print("Restarting the pumps.")


small_locke = Locke(5)
large_locke = Locke(10)

# Too many boats through a small locke will raise an exception
with small_locke as locke:
    locke.move_boats_through(8)
    print(f'{locke.boats} boats moving through small locke.')

# # A lock with sufficient capacity can move boats without incident.
# with small_locke as locke:
#     locke.move_boats_through(3)
#     print(f'{locke.boats} boats moving through small locke.')

# # Too many boats through a small locke will raise an exception
# with large_locke as locke:
#     locke.move_boats_through(12)
#     print(f'{locke.boats} boats moving through large locke.')

# # A lock with sufficient capacity can move boats without incident.
# with large_locke as locke:
#     locke.move_boats_through(8)
#     print(f'{locke.boats} boats moving through large locke.')
