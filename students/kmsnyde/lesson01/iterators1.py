# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

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
    def __init__(self, start=0, stop=5, step=1):
        self.start = start
        self.step = step
        super().__init__(stop=stop)
        self.current = self.start - 1
        
    def __iter__(self):
        return self
    
    def __next__(self):
        self.current += self.step
        if self.current < self.stop:
            return self.current
        else:
            raise StopIteration


if __name__ == "__main__":

    print("Testing the iterator_1")
    for i in IterateMe_1():
        print(i)
        
    print("\nTesting the iterator_2")
    for i in IterateMe_2(3, 20, 2):
        print(i)
   
    print("\nTesing a 'Break' after 10")
    it = IterateMe_2(2, 20, 2)
    for i in it:
        if i > 10:
            break
        print(i)
        # Stops printing when it hits 10
        
    print("\nPrint 'it'; picks up generator at 11")
    for i in it:
        print(i)
        # Since the generator state is at "11", picks up at 13.
    
