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

    def __init__(self, start=0, stop=5, step=1):
        self.current = start - 1
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
            
class IterateMe_2:
    def __init__(self, start=0, stop=5, step=1):
        self.current = start - step
        self.start = start
        self.stop = stop
        self.step = step

    def __iter__(self):
        #added the following line to get IterateMe_2 to work like range() - the count now starts over when a new loop is initiated.
        self.current = self.start - self.step
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
    print('Testing iterator_2')
    it = IterateMe_2(2, 20, 2)
    for i in it:
        if i > 10:
            break
        print(i)
    print('next')
    #when you break from the loop and try to pick it up again, it starts where it left off
    for i in it:
        print(i)
    #IterateMe_2 matches the function of range()
    #range is an iterable, not an iterator
