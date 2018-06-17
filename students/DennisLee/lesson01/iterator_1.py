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
    """An iterator similar to the range function."""

    def __init__(self, *args):
        if not args or len(args) > 3:
            raise TypeError("IterateMe_2 requires one to three arguments.")
        elif len(args) == 1:
            three_vals = (0, *args, 1)
        elif len(args) == 2:
            three_vals = (*args, 1)
        else:  # len(args) == 3
            three_vals = (*args,)
        (self.current, self.stop, self.step) = three_vals
        self.current -= self.step

    def __iter__(self):
        return self

    def __next__(self):
        self.current += self.step
        if (self.current < self.stop and self.step > 0) or (
                self.current > self.stop and self.step < 0):
            return self.current
        else:
            raise StopIteration


if __name__ == "__main__":

    print("Testing the iterator")
    for i in IterateMe_1():
        print(i)

    print("\nTesting the second iterator...")
    it = IterateMe_2(2, 20, 2)
    for i in it:
        if i > 10:  break
        print(i)
    print("Exited the first 'for' loop of the second iterator.")
    for i in it:
        print(i)

    print("\nTesting the second iterator using a range-like call...")
    print("\tImitate range(15):")
    it_range = IterateMe_2(15)
    for i in it_range:
        if i > 10:  break
        print(i)
    print("Exited the first 'for' loop of the second iterator.")
    for i in it_range:
        print(i)

    print("\tImitate range(20, 40):")
    it_range = IterateMe_2(20, 40)
    for i in it_range:
        if i > 30:  break
        print(i)
    print("Exited the first 'for' loop of the second iterator.")
    for i in it_range:
        print(i)

    print("\tImitate range(100, 50, -5):")
    it_range = IterateMe_2(100, 50, -5)
    for i in it_range:
        if i < 80:  break
        print(i)
    print("Exited the first 'for' loop of the second iterator.")
    for i in it_range:
        print(i)

    print("\nTry using the iterator again (it shouldn't work):")
    for i in it_range:
        print(i)
