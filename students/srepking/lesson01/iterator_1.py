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

    def __iter__(self):
        return IterateMe2(self.start,self.stop,self.step)



# If we wantered IterateMe_1 to behave more like range, we could create a seperate class to handle the iterator object.


class IterateMe2:
    def __init__(self, start, stop, step):
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

if __name__ == "__main__":

    print("Testing the iterator")
    for i in IterateMe_1():
        print(i)

    print("Testing again with start, stop, and step size set:")
    it = iter(IterateMe_1(2,20,2)) #'it' is an iterable object. You need to call __iter__ to get the iterator. Just like
    # in range.
    for i in it:
        if i > 10:
            break
        print(i)

    print("Try to pick up the iteration")
    print(i)
    print(next(it))



    print("Compare to range() function, you can't pick up where you left off unless you specifically "
          "create an iterator with iter(range()). So I proceed by creating an iterator of a range object.")
    range_it = iter(range(2,20,2))  # this is not an iterator object, and next() wont work on 'range_it'.
    for i in range_it:  # the for loop would create an iterator object,
                            # but I wound't be able to call it to continue the iteration after the break.
        if i > 10:
            break
        print(i)
    print("Try to pick up the range iteration")
    print(i)
    print(next(range_it))





