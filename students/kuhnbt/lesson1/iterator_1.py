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

    def __init__(self, start=False, stop=False, step=False):
        self.current = -1
        self.step = 1
        if not stop:
            if start:
                self.stop = start
            else:
                self.stop = 5
        else:
            self.stop = stop
            if step:
                self.step = step
            self.current = start - step
#Is there a simpler way to implement the above? The class needs to treat the first
#argument as 'stop' if there is only one argument, but otherwise the first argument 
#is 'start' and the second argument is 'stop'
            
    def __iter__(self):
        self.__init__()
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
