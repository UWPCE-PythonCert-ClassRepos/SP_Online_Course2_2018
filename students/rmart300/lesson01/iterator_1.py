#!/usr/bin/env python

"""
Simple iterator examples
"""

class IterateMe_2:

    def __init__(self, start, stop, step):
        self.start = start
        self.current = start
        self.stop = stop
        self.step = step

    def __iter__(self):
        self.current = self.start
        return self

    def __next__(self):
        next_iter = self.current
        self.current += self.step

        if next_iter < self.stop:
            return next_iter
        else:
            raise StopIteration

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


if __name__ == "__main__":

    print("Testing the iterator")
    for i in IterateMe_1():
        print(i)

    print("Testing iterator 2")
    it = IterateMe_2(2, 20, 2)
    for i in it:
        if i > 10:  break
        print(i)

    for i in it:
        print(i)

    print("Testing range")
    it = range(2,20,2)
    for i in it:
        if i > 10:  break
        print(i)

    for i in it:
        print(i)
