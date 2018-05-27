class IterateMe_2:

    def __init__(self, start=0, stop=None, step=1):
        if stop is None:
            self.curr = (-1) * step
            self.stop = start
        else:
            self.curr = start - step
            self.stop = stop
        self.next_step = step
        self.incr = self.curr < self.stop

    def __iter__(self):
        return self

    def __next__(self):
        self.curr += self.next_step
        if ((self.incr and self.curr < self.stop) or
            (not self.incr and self.curr > self.stop)):
            return self.curr
        else:
            raise StopIteration


if __name__ == "__main__":

    print("Testing the iterator")
    input("range(11)")
    for i in range(11):
        print(i)
    input("IterateMe_2(11)")
    for i in IterateMe_2(11):
        print(i)
    input("1 to 11")
    for i in IterateMe_2(1, 11):
        print(i)
    input("-5 to 5")
    for i in IterateMe_2(-5, 5):
        print(i)
    input("5 to -5")
    for i in IterateMe_2(5, -5, -1):
        print(i)
    input("-10 to -3 by 1")
    for i in IterateMe_2(-10, -3, 1):
        print(i)
    input("-3 to -10 by -2")
    for i in IterateMe_2(-3, -10, -2):
        print(i)
