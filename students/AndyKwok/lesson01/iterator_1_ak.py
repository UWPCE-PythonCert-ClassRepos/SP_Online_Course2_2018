# Author: Andy Kwok
# Last Updated: 10/23/18

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


class IterateMe_2:

    def __init__(self, start, stop=5, step=1):
        self.current = start - step
        self.stop = stop
        self.step = step

    def __iter__(self):
        return self

    def __next__(self):
        self.current += self.step
        if self.current < self.stop:
            return self.current
        else:
            raise StopIteration


if __name__ == "__main__":

    print("Testing the iterator")
    print("IterateMe_1:")
    for i in IterateMe_1():
        print(i, end =",")

    print("\nIterateMe_2:")
    it = IterateMe_2(2, 20, 2)
    for i in it:
        if i > 10: break
        print(i, end =",")

    for i in it:
        print(i, end =",")

    print("\nRange:")
    test = range(2, 20, 2)
    for n in test:
        print(n, end =",")
