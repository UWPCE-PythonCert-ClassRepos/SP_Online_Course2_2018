#!/usr/bin/env python

"""
Lesson 1 Assignment #2
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

'''
if __name__ == "__main__":

    print("Testing the iterator")
    for i in IterateMe_1():
        print(i)
'''

class IterateMe_2(IterateMe_1):
    def __init__(self,start,stop,step):
        self.current = -2+start
        self.stop = stop
        self.step = step

    def __next__(self):
        self.current += self.step
        if self.current < self.stop:
            return self.current
        else:
            raise StopIteration

if __name__ == "__main__":

    print("Testing the iterator")
    for i in IterateMe_2(start=2, stop=20, step=2):
        print(i)        

for n in range (2,20,2):
    print('range function: ',n)