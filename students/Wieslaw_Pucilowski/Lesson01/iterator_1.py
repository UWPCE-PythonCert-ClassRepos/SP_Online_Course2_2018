#!/usr/bin/env python

"""
Simple iterator examples
"""
__author__="Wieslaw Pucilowski"


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

    def __init__(self, start, stop, step=1):
        self.current = start
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

    print("Testing the iterator 1")
    for i in IterateMe_1(20):
        print(i)

    print("Testing the iterator 2")
    for i in IterateMe_2(0,20,2):
        print(i)