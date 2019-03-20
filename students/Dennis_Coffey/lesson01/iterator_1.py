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
        raise StopIteration

class IterateMe_2:
    """
    Iterator to generate a range
    """

    def __init__(self, *args):
        # Set defaults
        self.step = 1
        self.start = 0
        if not args:
            raise TypeError("IterateMe_2 requires between one and three arguments.")
        elif len(args) == 1:
            self.stop = args[0]
        elif len(args) == 2:
            self.start = args[0]
            self.stop = args[1]
        elif len(args) == 3:
            self.start = args[0]
            self.stop = args[1]
            self.step = args[2]
            
        self.current = self.start - self.step

    def __iter__(self):
        self.current = self.start - self.step # Added in so iterator acts like range if there is a break
        return self

    def __next__(self):
        self.current += self.step
        if self.current < self.stop:
            return self.current
        raise StopIteration

if __name__ == "__main__":

    print("Testing the iterator 1")
    for i in IterateMe_1():
        print(i)

    print("Testing the iterator 2")
    for i in IterateMe_2(2, 20, 2):
        print(i)
        
    print("Testing the iterator 2 with a break")
    it = IterateMe_2(2, 20, 2)
    for i in it:
        if i > 10:  break
        print(i)
    for i in it:
        print(i)
        
    print("Testing the range function with a break")
    range_test = range(2, 20, 2)
    for i in range_test:
        if i > 10:
            break
        print(i)
    for i in range_test:
        print(i)       

    # Test whether IterateMe_2 produces same result as range for different scenarios
    assert list(IterateMe_2(10)) == list(range(10)), "Does not work like range"
    assert list(IterateMe_2(4,15)) == list(range(4,15)), "Does not work like range"
    assert list(IterateMe_2(3,44,3)) == list(range(3,44,3)), "Does not work like range"

