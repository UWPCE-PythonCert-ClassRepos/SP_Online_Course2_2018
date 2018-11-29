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
    """
    About as simple an iterator as you can get:

    returns the sequence of numbers from zero to 4
    ( like range(4) )
    """

    def __init__(self, start, stop, step=1):
        self.current = start - 1
        self.start = start
        self.stop = stop
        self.step = step

    def __iter__(self):
        self.current = self.start-1
        return self

    def __next__(self):
        self.current += self.step
        if self.current < self.stop:
            return self.current
        else:
            raise StopIteration


if __name__ == "__main__":

    print("Testing the iterator")
    for i in IterateMe_1():
        print(i)

    it = IterateMe_2(2, 20, 1)
    for i in it:
        if i > 10:  break
        print(i)

    for i in it:
        print(i)

    print("Testing Range function")
    r = range(2, 20, 1)
    for i in r:
        if i > 10:  break
        print(i)

    for i in r:
        print(i)