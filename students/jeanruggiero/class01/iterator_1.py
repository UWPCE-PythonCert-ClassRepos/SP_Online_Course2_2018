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

class IterateMe_2():
    """
    This one returns an iterable that acts more like range.
    (range is an interable).
    """

    def __init__(self, start, stop, step=1):
        self.current = start-step
        self.stop = stop
        self.step = step
        self.start = start

    def __iter__(self):
        # Start over at the beginning each time the instantiation is iterated
        # over.
        self.current = self.start-self.step
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
        if i > 50:
            break

    # This iterator acts like range
    print('\nTesting iterator 2')
    for i in IterateMe_2(0,5,2):
        print(i)

    print()
    # Here we iterate over the same instantiation multiple times, picking up
    # at the beginning each time.
    it = IterateMe_2(2, 20, 2)
    for i in it:
        if i > 10:
            break
        print(i)

    print()
    for i in it:
        print(i)
