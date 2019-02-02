#!/usr/bin/python
#Lesson 3 Aurel Perianu

"""
    Context Managers - Ballard locks
"""

class Locke(object):
    """
        define class locks
    """
    def __init__(self, capacity=1):
        capacity = int(capacity)
        if capacity < 1:
            raise ValueError("Capacity must be a positive integer, try again")
        else:
            self.capacity = capacity

    def __enter__(self):
        print("Stopping the pumps.")
        print("Opening the doors.")
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if exception_type is None:
            print("Closing the doors.")
            print("Restarting the pumps.")
            print('Finish __exit__ locke.\n')
        else:
            print('\nCannot pass boats: {} {}'.
                  format(exception_type, exception_value))
            print("Closing the doors.")
            print("Restarting the pumps.")
        return True

    def move_boats_through(self, nr):
        nr = int(nr)
        if nr > self.capacity:
            raise ValueError("\nNumber of boats:{} exceeds locke capacity:{}\n"
                            .format(nr, self.capacity))
        print("\nMoving {} boats through locke.\n".format(nr))

if __name__ == "__main__":

    small_locke = Locke(5)
    large_locke = Locke(10)
    boats = 7

    print('\nnumber of boats: {}'.format(boats))
    print("\ntesting large lock\n")
    # A lock with sufficient capacity can move boats without raising an exception.
    with large_locke as locke:
        locke.move_boats_through(boats)

    print("\ntesting small lock\n")
    # Too many boats through a small locke will raise an exception
    with small_locke as locke:
        locke.move_boats_through(boats)

    boats = 4
    print('\nnumber of boats: {}'.format(boats))
    print("\ntesting large lock\n")
    # A lock with sufficient capacity can move boats without raising an exception.
    with large_locke as locke:
        locke.move_boats_through(boats)

    print("\ntesting small lock\n")
    # Small nr of boats through a small locke will not raise an exception.
    with small_locke as locke:
        locke.move_boats_through(boats)

    boats = 11
    print('\nnumber of boats: {}'.format(boats))
    print("\ntesting large lock\n")
    # Too many boats will raise an execption
    with large_locke as locke:
        locke.move_boats_through(boats)

    print("\ntesting small lock\n")
    # Too many boats will raise an execption
    with small_locke as locke:
        locke.move_boats_through(boats)
