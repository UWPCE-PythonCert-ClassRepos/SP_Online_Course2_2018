#!/usr/bin/env python
""" Simple iterator examples """

class IterateMe_1:
    """
    Simple iterator - returns the sequence of numbers from zero to 4
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


class IterateMe_2():
    """ Iterator designed to match functionality of 'range' """
    
    def __init__(self, start, stop, step=1):
        self.start = start
        self.stop = stop
        self.step = step
        self.values = [val for val in self.collection()]

    def collection(self):
        current = self.start
        while current < self.stop:
            yield(current)
            current += self.step 

    def __iter__(self):
        return iter(self.values)

    def __getitem__(self, index):
        return self.values[index]

    def __repr__(self):
        return "IterateMe_2({}, {}, {})".format(self.start, self.stop, self.step)
    

if __name__ == "__main__":

    print("Testing iterator_1")
    for i in IterateMe_1():
        print(i)

    print("\nTesting iterartor_2")
    it = IterateMe_2(2, 20, 2)

    for i in it:
        if i > 10: break
        print(i)
    print("Breaking after 10...\n")
    
    print("Picking up after breaking...")
    for i in it:
        print(i)
        

