#!/usr/bin/env python

"""
Simple iterator examples
"""
import future
import builtins
import past
import six


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

    def next(self):
        return self.__next__()


if __name__ == "__main__":

    print("Testing the iterator")
    for i in IterateMe_1():
        print(i)
