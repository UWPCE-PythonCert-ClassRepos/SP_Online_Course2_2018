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
    def __init__(self, start, stop, step=1):
        self.stop = stop
        self.step = step

        if step == 0:
            raise ValueError
        elif step == 1:
            self.current = -step
        else:
            self.current = start-step

    def __iter__(self):
        return self

    def __next__(self):
        self.current += self.step
        if self.current < self.stop:
            return self.current
        else:
            raise StopIteration


class IteratorLikeRange:
    def __init__(self, start, stop, step=1):
        self.stop = stop
        self.step = step

        if step == 0:
            raise ValueError
        elif step == 1:
            self.current = -step
        else:
            self.current = start-step

    def __iter__(self):
        # return self
        self.next = self.current + self.step
        return IteratorLikeRange(self.next, self.stop, self.step)

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

    print("Testing the iterator 2")
    it = IterateMe_2(-1, 5)
    for i in it:
        print(i)

    print("Testing the iterator 2 with step")
    it = IterateMe_2(2, 20, 2)
    for i in it:
        if i > 10:
            break
        print(i)

    for i in it:
        print(i)

    # range returns an iterable
    # that can be converted to an iterator with iter(range(2, 20, 2))
    print("Testing range")
    r = range(2, 20, 2)
    for i in r:
        if i > 10:
            break
        print(i)

    for i in r:
        print(i)

    print("Testing IteratorLikeRange")
    ir = IteratorLikeRange(2, 20, 2)
    for i in ir:
        if i > 10:
            break
        print(i)

    for i in ir:
        print(i)
