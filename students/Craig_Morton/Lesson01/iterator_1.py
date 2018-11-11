# ------------------------------------------------- #
# Title: Lesson 1, pt 2, Iterators Assignment
# Dev:   Craig Morton
# Date:  11/6/2018
# Change Log: CraigM, 11/6/2018, Iterators Assignment
# ------------------------------------------------- #

# !/usr/bin/env python3


class IterateMe_1:
    """Simple iterator that returns the sequence of numbers from 0 to 4 (like range(4))"""
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


class IterateMe_2:
    """Like IterateMe_1, but similar to range()"""
    def __init__(self, start, stop, step):
        self.current = start - step
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

    print("\nBegin IterateMe_1 testing:")
    for i in IterateMe_1():
        print(i)

    print("\nBegin IterateMe_2 testing:")
    iterate = IterateMe_2(2, 20, 2)
    for i in iterate:
        if i > 10:
            break
        print(i)
    for i in iterate:
        print(i)

    print("\nBegin range() testing:")
    use_range = range(2, 20, 2)
    for i in use_range:
        if i > 10:
            break
        print(i)
    for i in use_range:
        print(i)
