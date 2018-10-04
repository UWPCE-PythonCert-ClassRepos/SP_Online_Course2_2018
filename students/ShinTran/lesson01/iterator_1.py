'''
Shin Tran
Python 220
Lesson 1 Assignment
'''

#!/usr/bin/env python


# Simple iterator examples



class IterateMe_1:
    """
    About as simple an iterator as you can get:
    returns the sequence of numbers from zero to 4
    ( like range(4) )
    """

    def __init__(self, stop = 5):
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
    # Extends InterateMe_1, added a start and step parameter
    def __init__(self, start, stop, step = 1):
        self._current = start - step
        self._start = start
        self._stop = stop
        self._step = step

    def __iter__(self):
        # An iteration will start over instead of continue after a break
        self._current = self._start - self._step
        return self

    def __next__(self):
        self._current += self._step
        if self._current < self._stop:
            return self._current
        else:
            raise StopIteration

if __name__ == "__main__":
    
    print("Testing the iterator:")
    list1 = []
    for i in IterateMe_1():
        list1.append(i)
    print(list1)
    
    print("Testing the iterator 2:")
    list2a = []
    list2b = []
    it = IterateMe_2(2, 20, 2)
    for j in it:
        if j > 10:
            break
        list2a.append(j)
    print(list2a)
    print("What does it print after a break?")
    for j in it:
        list2b.append(j)
    print(list2b)
    
    print("Using the Range function:")
    list3a = []
    list3b = []
    rg = range(3, 30, 3)
    for k in rg:
        if k > 15:
            break
        list3a.append(k)
    print(list3a)
    print("After the break:")
    for k in rg:
        list3b.append(k)
    print(list3b)