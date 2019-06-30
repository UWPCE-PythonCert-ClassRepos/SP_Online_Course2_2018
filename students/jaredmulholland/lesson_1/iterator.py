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

"""Extend (iterator_1.py ) to be more like range() – add three input parameters: iterator_2(start, stop, step=1)"""

class Iterator_2:

    def __init__(self, start, end, step):
        self.value = start
        self.end = end
        self.step = step

    def __iter__(self):
        return self

    def __next__(self):
        if self.value < self.end:
            current = self.value
            self.value += self.step
            return current
        else:
            raise StopIteration

"""
Iterator Questions:
1. IterateMe_2 does not work exactly like range
2. Iterator_2 does work like range
3. Range is an iterable, not an iterator
"""