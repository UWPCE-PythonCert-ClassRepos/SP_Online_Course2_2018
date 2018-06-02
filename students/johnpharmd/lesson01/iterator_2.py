#!/usr/bin/env python
from itertools import count
"""
Simple iterator examples
"""


class IterateMe_1:
    """
    About as simple an iterator as you can get:

    returns the sequence of numbers from zero to 4
    ( like range(5) )
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
    Extends IterateMe_1 to be more like range
    """

    def __init__(self, start=0, stop=None, step=1):
        self.start = start
        self.current = start
        self.stop = stop
        self.step = step
        self.count = count()

    def __iter__(self):
        return self

    def __next__(self):
        if not next(self.count):
            return self.start 
        else:
            try:
                self.current += self.step
                assert self.current < self.stop
                next(self.count)
                return self.current
            except AssertionError:
                raise StopIteration


if __name__ == "__main__":

    print("Testing the iterators")
    print("IterateMe_1:\n")
    for i in IterateMe_1():
        print(i)

    print("\nIterateMe_2(0, 7):\n")
    for i in IterateMe_2(0, 7):
        print(i)

    print("Break from loop then try to restart loop:")
    print("""
    it = IterateMe_2(2, 20, 2)
    for i in it:
        if i > 10:  break
        print(i)

    for i in it:
        print(i)
    """)
    it = IterateMe_2(2, 20, 2)
    for i in it:
        if i > 10:
            break
        print(i)

    for i in it:
        print(i)
    # Result is that 'for' loop breaks when i=12. If loop is restarted, it begins at i=12,
    # rather than at i=2. Range, OTOH, returns to i=2.