#!/usr/bin/env python3

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

class Iterator_2(IterateMe_1):

    def __init__(self, start, stop, step=1):
        self.current = start
        self.start = start
        self.stop = stop
        self.step = step

    def __iter__(self):
        self.current =self.start
        return self

    def __next__(self):
        self.current += self.step
        if self.current < self.stop:
            return self.current
        else:
            raise StopIteration

if __name__ == "__main__":

    print("Testing the IterateMe_1")

    it1 = IterateMe_1(20)
    for i in it1:
        if i > 10: break
        print(i)

    for i in it1:
        print(i)

    print("Testing the Iterator_2")
    it = Iterator_2(2,20,2)
    for i in it:
        if i > 10: break
        print(i)

    for i in it:
        print(i)

    print("Testing range()")
    r = range(2,20,2)
    for i in r:
        if i > 10: break;
        print(i)

    for i in r:
        print(i)