#!/usr/bin/env python

"""
Simple iterator examples
"""


class IterateMe_1:
    """
    About as simple an iterator as you can get:

    returns the sequence of numbers from zero to 4
    ( like range(4) )
    """

    def __init__(self, stop=5):
        self.current = -1
        self.stop = stop

    def __iter__(self):
        return self

    def __next__(self):
        self.current += 1
        if self.current < self.stop:
            return self.current
        else:
            raise StopIteration


class IterateMe_2(IterateMe_1):
    """
    Extension of IterateMe_1 to make it more like range().
    """

    def __init__(self, start, stop, step=1):
        self.current = start - step
        self.stop = stop
        self.step = step

    def __next__(self):
        self.current += self.step
        if self.current < self.stop:
            return self.current
        else:
            raise StopIteration


if __name__ == "__main__":

    print("Testing IterateMe_1:")
    for i in IterateMe_1():
        print(i)

    print("\nTesting IterateMe_2, as compared to IterateMe_1:")
    for i in IterateMe_2(20, 60, 5):
        print(i)

    print("\nrange() testing:")
    it = range(2, 20, 2)
    for i in it:
        if i > 10:
            break
        print(i)
    for i in it:
        print(i)

    print("\nIterateMe_2 with same inputs as previous range() testing:")
    it = IterateMe_2(2, 20, 2)
    for i in it:
        if i > 10:
            break
        print(i)
    for i in it:
        print(i)

# range() resets to the very beginning every time it is instantiated, making it an iterable rather than an iterator.
# Because IterateMe_2 is an iterator, it restarts from the point that it breaks (12) rather than the beginning.
