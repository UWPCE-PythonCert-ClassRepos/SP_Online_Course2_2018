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
    Extends IterateMe_2
    """

    def __init__(self, start, stop, step=1):
        super().__init__(stop)
        self.start = start
        self.current = start - step
        self.step = step

    def __iter__(self):
        self.current = self.start - self.step
        return self

    def __next__(self):
        self.current += self.step
        if self.current < self.stop:
            return self.current
        else:
            raise StopIteration


if __name__ == "__main__":

    # Test IterateMe_1
    print("Testing the iterator")
    for i in IterateMe_1():
        print(i)

    # Test IterateMe_2
    test_it = IterateMe_2(3, 30, 3)
    for i in test_it:
        print(i)

    # Test Range for what it does
    range_test = range(2, 20, 2)
    for i in range_test:
        if i > 10:
            break
        print(i)
    for i in range_test:
        print(i)

    # Make IterateMe_2 match Range
    it = IterateMe_2(2, 20, 2)
    for i in it:
        if i > 10:
            break
        print(i)
    for i in it:
        print(i)
