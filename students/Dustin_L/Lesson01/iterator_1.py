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
        self.curr = -1
        self.stop = stop

    def __iter__(self):
        return self

    def __next__(self):
        self.curr += 1
        if self.curr < self.stop:
            return self.curr
        else:
            raise StopIteration


class IterateMe_2(IterateMe_1):
    """Extends IterateMe_1

    Uses start, stop and step params
    """
    def __init__(self, start, stop, step=1):
        super().__init__(stop=stop)
        self.curr = start - step
        self.strt = start
        self.step = step

    def __iter__(self):
        self.curr = self.strt - self.step
        return self

    def __next__(self):
        self.curr += self.step
        if self.curr < self.stop:
            return self.curr
        else:
            raise StopIteration


if __name__ == "__main__":
    print("Testing the iterator")
    for i in IterateMe_1():
        print(i)

    print("Testing iterator 2")
    for i in IterateMe_2(3, 10, 2):
        print(i)

    print("Testing stopping and starting")
    it = IterateMe_2(2, 20, 2)
    # it = range(2, 20, 2)
    for i in it:
        if i > 10:
            break
        print(i)
    for i in it:
        print(i)
