'''
Shin Tran
Python 220
Lesson 3 Assignment
'''

# Implementing the Ballard Locks using a context manager

class Locke(int):
    
    def __init__(self, limit):
        self._limit = limit
        print("    Locke capacity is {}.".format(limit))

    def __enter__(self):
        print("    Stoping the pumps.")
        print("    Opens the doors.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            print(exc_val)
        print("    Closing the doors.")
        print("    Starting the pumps.")
        print()
        return self

    def move_boats_through(self, num_boats):
        if num_boats <= self._limit:
            print("    Moving {} boats throguh.".format(num_boats))
        else:
            s = "    The number of boats trying to pass through, {}. exceeds the capacity of {}."
            raise Exception(s.format(num_boats, self._limit))

if __name__ == "__main__":
    boats = 8

    print("Letting boats through the large locke:")
    large_locke = Locke(10)
    # A lock with sufficient capacity can move boats without incident
    with large_locke as locke:
        locke.move_boats_through(boats)

    print("Letting boats through the small locke:")
    small_locke = Locke(5)
    # Too many boats through a small locke will raise an exception
    with small_locke as locke:
        locke.move_boats_through(boats)

    print("Letting boats through the medium locke:")
    medium_locke = Locke(7)
    # A lock with sufficient capacity can move boats without incident
    with medium_locke as locke:
        locke.move_boats_through(boats)