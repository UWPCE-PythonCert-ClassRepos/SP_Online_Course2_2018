#!/usr/bin/env python3

"""Extend (iterator_1.py ) to be more like range() 
add three input parameters: iterator_2(start, stop, step=1)
What happens if you break from a loop and try to pick it up again:
it = IterateMe_2(2, 20, 2)
for i in it:
    if i > 10:  break
    print(i)
for i in it:
    print(i)
Does range() behave the same?
make yours match range()
is range an iterator or an iteratable?
--range is an iteratable not an iterator
"""

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
    """Extending IterateMe_1"""

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

    print("Testing iterator One")
    for i in IterateMe_1():
        print(i)

    print("Testing iterator Two")
    it = IterateMe_2(2, 20, 2)
    for i in it:
        if i > 10:
            break
        print(i)
    for i in it:
        print(i)
