#!/usr/bin/env python

"""
Simple iterator examples
"""


class IterateMe_1:
    """
    Creating an iterator that behaves more like range() so that you need to explicitly call iter()
    to create an iterator and use the next() function.
    """

    def __init__(self, start=0, stop=5, step=1):
        self.current = start-step
        self.stop = stop
        self.start = start
        self.step = step

    def __next__(self):
        self.current += self.step
        if self.current < self.stop:
            return self.current
        else:
            raise StopIteration

    def __iter__(self):
        return IterateMe_helper(self.start,self.stop,self.step)

class IterateMe_helper:
    """This class is used to generate an interator for the IterateMe_1 Class, so that everytime the for loop is
    used on an IterateMe_1 instance, a new iterator is created."""

    def __init__(self, start=0, stop=5, step=1):
        self.current = start-step
        self.stop = stop
        self.start = start
        self.step = step

    def __next__(self):
        self.current += self.step
        if self.current < self.stop:
            return self.current
        else:
            raise StopIteration

    def __iter__(self):
        return self




# Or create this class that behaves like Range because we are using the range function.


class PsuedoRange:
    def __init__(self, start=0, stop=5, step=1):
        self.current = start-step
        self.stop = stop
        self.start = start
        self.step = step
        self.range = range(start, stop, step)


    def __iter__(self):
        for n in self. range:
            yield int(n)



if __name__ == "__main__":

    print("Testing PsuedoRange")
    for i in PsuedoRange():
        print(i)

    print("Testing PsuedoRange again with start, stop, and step size set:")
    it = PsuedoRange(2,20,2)
    for i in it:
        if i > 10:
            break
        print(i)

    print("Emulating range with PsuedoRange, so the cycle should start again after break")
    for i in it:
        print(i)


    print("Testing IterateMe_1:")
    it = IterateMe_1(2,20,2)
    for i in it:
        if i > 10:
            break
        print(i)

    print("Emulating range with IterateMe_1, so the cycle should start again after break")
    for i in it:
        print(i)


    print("Now Testing Range")
    range_it = range(2,20,2)
    for i in range_it:

        if i > 10:
            break
        print(i)
    print("The real range after break:")
    for i in range_it:
        print(i)






