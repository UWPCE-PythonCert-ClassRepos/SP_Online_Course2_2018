"""
Iterators & Iterables
"""

class IterateMe_1:
    def __init__(self, stop=5):
        self.current = 0
        self.stop = stop
    def __iter__(self):
        return self
    def __next__(self):
        if self.current < self.stop:
            self.current += 1
            return self.current
        else:
            raise StopIteration


"""
    Extend (iterator_1.py ) to be more like range() – add three input parameters: iterator_2(start, stop, step=1)
    What happens if you break from a loop and try to pick it up again:

it = IterateMe_2(2, 20, 2)
for i in it:
    if i > 10:  break
    print(i)

for i in it:
    print(i)

    Does range() behave the same?
        make yours match range()
        is range an iterator or an iteratable? 
"""