#!/usr/bin/env python

"""
Simple iterator examples
"""

class IterateMe_2:
    def __init__(self, start=0, stop=5, step=1):
        self.current = start-step
        self.stop = stop
        self.step = step

    def __iter__(self):
        return IterateMe_2_iter(self.current+self.step, self.stop, self.step)



class IterateMe_2_iter:
    """
    About as simple an iterator as you can get:

    returns the sequence of numbers from zero to 4
    ( like range(4) )
    """

    def __init__(self, start=0, stop=5, step=1):
        self.current = start-step
        self.stop = stop
        self.step = step

    def __iter__(self):
        return self

    def __next__(self):
        self.current += self.step
        if self.current < self.stop:
            return self.current
        else:
            raise StopIteration

    def next(self):
        return self.__next__()


if __name__ == "__main__":

    print("Testing the iterator")
    for i in IterateMe_2():
        print(i)

    print("\n Test that iterator matches range() function \n")
    print("iterator output")
    it = IterateMe_2(2,20,2)
    for i in it:
        if i>10: break
        print(i)
    print("\n Does iterator generate new iterator in a new for loop:")
    for i in it:
        print(i)
    print("\n If we do the same with the range() function: \n")
    it = range(2,20,2)
    for i in it:
        if i>10: break
        print(i)
    print("\n Does the range() function generate new iterator in a new for loop:")
    for i in it:
        print(i)
