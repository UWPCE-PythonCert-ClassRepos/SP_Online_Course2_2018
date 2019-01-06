#!/usr/bin/env python3

"""
Lesson 2 Assignment: Iterators and Iterables
Answer to question: range is an iterable
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
    Extended iterator_1 to be more like range
    """

    def __init__(self, start, stop, step=1):
        self.current = start - step
        self.start = start
        self.stop = stop
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

    print("Testing the iterator")
    for i in IterateMe_1():
        print(i, end=' ')

    print("\n\nTesting the improved iterator")
    for i in IterateMe_2(0, 5):
        print(i, end=' ')

    print("\n\nTesting improved iterator compared to range")
    it = IterateMe_2(2, 20, 2)
    for i in it:
        if i > 10: break
        print(i, end=' ')
    print("pause",end=' ')
    for i in it:
        print(i, end=' ')

    print("\n\nCompare to range")
    rng = range(2, 20, 2)
    for r in rng:
        if r > 10: break
        print(r, end=' ')
    print("pause", end=' ')
    for r in rng:
        print(r, end=' ')
