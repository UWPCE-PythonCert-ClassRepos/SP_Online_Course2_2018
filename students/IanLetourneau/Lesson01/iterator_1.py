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


class IterateMe_2:
    """An iteration object that functions
    similarly to the built-in range() function"""

    def __init__(self, start, stop, step=1):
        """Initializer utulizing added start and
        step parameters."""

        self.current = start-step
        self.start = start
        self.stop = stop
        self.step = step

    def __iter__(self):
        """Iterator function that will restart
        generator should the call loop be broken"""

        self.current = self.start-self.step
        return self

    def __next__(self):
        """Iterator function that will grab next
        value in iteration sequence until maximum
        value is reached."""

        self.current += self.step
        if self.current < self.stop:
            return self.current
        else:
            raise StopIteration


if __name__ == "__main__":

    # Test The initial iterator class
    print("Testing the iterator")
    for i in IterateMe_1():
        print(i)

    # Test newly created iterator class
    print("Testing new iterator")
    for i in IterateMe_2(2, 20, 2):
        print(i)

    # Test stopping iteration loop midway
    print("Testing break in iterator")
    it = IterateMe_2(2, 20, 2)
    for i in it:
        if i > 10:
            break
    print(i)
    for i in it:
        print(i)

    # Test breaking iteration loop in
    # range() function
    print("Testing break in range")
    r = range(2, 20, 2)
    for i in r:
        if i > 10:
            break
    print(i)
    for i in r:
        print(i)
