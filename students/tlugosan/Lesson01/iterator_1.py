#!/usr/bin/env python3


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


class IterateMe_2(IterateMe_1):
    def __init__(self, start, stop, step=1):
        self.current = start + step
        self.start = start
        self.stop = stop
        self.step = step

    def __iter__(self):
        self.current = self.start + self.step
        return self

    def __next__(self):
        if self.current < self.stop:
            self.current += self.step
            return self.current
        else:
            raise StopIteration


if __name__ == "__main__":

    print("IterateME_1")
    for i in IterateMe_1():
        print(i)

    print("IterateME_2")
    it = IterateMe_2(2, 20, 2)
    for i in it:
        if i > 10: break
        print(i)

    print("-----------------------")
    for i in it:
        print(i)
