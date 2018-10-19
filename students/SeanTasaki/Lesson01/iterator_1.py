#!/usr/bin/env python3
#Sean Tasaki
#10/18/2018

"""
Simple iterator examples
"""


class IterateMe_1:
 
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
    def __init__(self, start, stop, step=1):
        super().__init__(stop=stop)
        self.current = start - step
        self.start = start
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

    print("Testing the iterator")
    for i in IterateMe_1():
        print(i)

    print("\nTesting the iterator2:")

    it = IterateMe_2(2, 20, 2)
    for i in it:
        if i > 10:
            break
        print(i)
        
    for i in it:
        print(i)

    print("\nTesting the range:")
    
    for i in range(2, 20, 2):
        if i > 10:
            break
        print(i)
                
    for i in range(2, 20, 2):
        print(i)