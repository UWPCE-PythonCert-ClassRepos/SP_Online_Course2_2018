#lesson 01 extending iterators
#!/usr/bin/env python3

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
    """ 
    A class similar to range
    """
    def __init__(self, start, stop, step=1):
        super().__init__(stop=stop)
        self.current = start - step
        self.start = start
        self.step = step
    
    def __next__(self):
        self.current += self.step
        if self.current < self.stop:
            return self.current
        else:
            raise StopIteration
        
class IterateMe_3(IterateMe_2):
    """
       A class more similiar to range
    """
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

    print("Testing the iterator")
    for i in IterateMe_1():
        print(i)

    print("Testing the second iterator")
    it = IterateMe_2(2, 20, 2)
    for i in it:
        if i > 10:  break
        print(i) 
    for i in it:
        print(i)
    # 12 doesn't get printed because the first for loop breaks without printing
    # the second for loop starts back up at the interrupted value and continues
    
    print("Testing range")
    it = range(2, 20, 2)
    for i in it:
        if i > 10:  break
        print(i) 
    for i in it:
        print(i)
    # range breaks on 12 in the first for loop
    # the second for loop resets to the original start
    # range is an iterable (has __iter__) but not an iterator (does not have __next__)
    
    print("Testing the third iterator")
    it = IterateMe_3(2, 20, 2)
    for i in it:
        if i > 10:  break
        print(i) 
    for i in it:
        print(i)
    # reacts like range after the first for loop is broken because __iter__ 
    # resets self.current to the original value