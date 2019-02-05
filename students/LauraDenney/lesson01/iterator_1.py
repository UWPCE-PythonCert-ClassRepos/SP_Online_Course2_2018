#-------------------------------------------------#
# Title: Iterator Exercise
# Dev:   LDenney
# Date:  February 3rd, 2019
# ChangeLog: (Who, When, What)
#   Laura Denney, 2/3/19, Started work on Iterator Exercise
#-------------------------------------------------#

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
    def __init__(self, start=0, stop = 5, step = 1):
        self.current = start - step
        self.start = start
        self.stop = stop
        self.step = step

    def __iter__(self):
        return self.myrange()

    def myrange(self):
        start = self.start
        stop = self.stop
        step = self.step
        while start < stop:
            yield start
            start += step



    # def __next__(self):
    #     self.current += self.step
    #     if self.current < self.stop:
    #         return self.current
    #     else:
    #         raise StopIteration

if __name__ == "__main__":

    print("Testing the iterator")
    test = IterateMe_2(stop = 20)
    for i in test:
        if i == 10:
            break
        print(i)
    print("After break")
    for i in test:
        print(i)

    print("Now, comparing to range()")
    test = range(0,20)
    for i in test:
        if i == 10:
            break
        print(i)
    print("After break")
    for i in test:
        print(i)
