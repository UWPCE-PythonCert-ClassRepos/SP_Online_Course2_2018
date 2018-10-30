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
    iterator builder:
    IterateMe_2(start, stop , step = 0)
    returns the sequence of numbers from "start" to "stop" by "step"
    """

    def __init__(self, start=0, stop=5, step=1):
        if start > stop:
            raise Exception('"start" should not exceed "stop"')
        self.start = start - step
        self.stop = stop
        self.step = step

    def __iter__(self):
        self.current = self.start
        return self

    def __next__(self):
        self.current += self.step
        if self.current < self.stop:
            return self.current
        else:
            raise StopIteration


if __name__ == "__main__":

    print("Testing IterateMe_1")
    for i in IterateMe_1():
        print(i)

    print("Testing IterateMe_2")
    for i in IterateMe_2():
        print(i)

