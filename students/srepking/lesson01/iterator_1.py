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

    def __init__(self, start=0, stop=5, step=1):
        self.current = start-step
        self.stop = stop
        self.start = start
        self.step = step

    def __iter__(self):
        return self  # we can return a seperate iterator object if we don't want this to be an iterator
        #  without first being requested with iter().

    def __next__(self):
        self.current += self.step
        if self.current < self.stop:
            return self.current
        else:
            raise StopIteration


# If we wantered Iterator_1 to behave more like range, we could create a seperate class to handle the iterator object.

class NewRange:
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
    it = IterateMe_1(2,20,2) #this is actually an iterator object, and next(it) will iterate through
    for i in it: #the for loop internally creates an iterator object by calling iter(it).
        if i > 10:
            break
        print(i)

    print("Now try to pickup the count again")
    print(next(it))
    #The iterator continues on, though it does miss one number do the programming in __next__.

    print("Compare to range() function, you can't pick up where you left off unless you specifically "
          "create an iterator with iter(range()). So I procede by creating an iterator of a range object.")
    range_it = range(2,20,2)  # this is not an iterator object, and next() wont work on 'range_it'.
    iter_range = iter(range_it)  # so we create an iterator object so next() works.
    for i in iter_range:  # the for loop would create an iterator object,
                            # but I wound't be able to call it to continue the iteration after the break.
        if i > 10:
            break
        print(i)

    print("Using the iter() function to get the iterator of the range object, \n"
          "we can get range to behave like IterateMe_1."
          "Using next(),\n we can pick up iteration after the break.")
    print(next(iter_range))
    print("\n I also created a new class called NewRange that behaves more like the range() function. "
          "\n You need to explicitly call iter() on it to create an iterator object.")
    range_new= NewRange(2,20,2)
    for i in range_new:  # We can iterate over it with a for loop
        print(i)

    # but if you call next(range_new), it won't work, because it is not an iterator.

    print(next(range_new))
# Does the range() behave the same?
# No, the 'range()' object is not an iterator,
# but it is iterable.
# The IterateMe_1() object is an iterator.
# With range, You can use the iter() function to return an iterator,
# and iterate through the range of the object with next().




