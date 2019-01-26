#!/usr/bin/env python
# Lesson1 - Aurel Perianu

class IterateMe_2:
    """
        A more complex iterator:
        returns the sequence of numbers from start to stop  with step
    """

    def __init__(self, start=1, stop=10, step=1):
        self.start = start
        self.stop = stop
        self.step = step

    def __iter__(self):
        self.current = self.start - self.step
        return self

    def __next__(self):
        self.current += self.step
        if self.current < self.stop:
            return self.current
        else:
            raise StopIteration


if __name__ == "__main__":

    print("Testing the iterator (default values):")
    for i in IterateMe_2():
        print(i)

    print("\nTesting the iterator (2, 20, 2):")
    for i in IterateMe_2(2, 20, 2):
        print(i)
    print('\n\nIterator vs range with break:\n')

    it = IterateMe_2(1, 11, 1)
    for i in it:
        if i > 5:
            print("interrupt iterator at: ", i)
            break
        print(i)
    print("\nIterator after break (restart count):")
    #iterator continues from the value where we break
    for i in it:
        print(i)

    print ('\nPrint range with break:')
    range_x = range(1,11,1)
    for i in range_x:
        if i > 5:
            print("interrupt range at: ", i)
            break
        print(i)

    print ("\nprint using range after break ")
    for i in range_x:
        print (i)
    #print(dir(range))
    #print("range vs iterator: range has no __next__ method")
