#!/usr/bin/env python

"""
Lesson01 - Iterators & Iteratables
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

    def __init__(self, start, stop, step=1):
        self.start = start
        self.stop = stop
        self.step = step
        self.current = start

    def __iter__(self):
        self.current = self.start - self.step
        return self

    def __next__(self):

        self.current += self.step

        if self.current - self.step == self.start:
            self.start

        if self.current < self.stop:
            return self.current
        else:
            raise StopIteration


if __name__ == "__main__":
    it = IterateMe_2(2, 20, 2)
    print('First loop...')
    for i in it:
        if i > 10:
            break
        print(i)
    print('\n\nSecond loop...')
    for i in it:
        print(i)
