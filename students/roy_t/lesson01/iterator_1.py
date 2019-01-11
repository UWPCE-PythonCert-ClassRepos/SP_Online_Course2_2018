#!/usr/bin/env python3

class IterateMe_2:

    def __init__(self, start, stop, step=1):
        self.start = start
        self.stop = stop
        self.step = step

    def interator_2(self, start, stop, step=1):


def main():
    it = IterateMe_2(2, 20, 2)
    for i in it:
        if i > 10:  break
        print(i)
    for i in it:
        print(i)

if __name__ == "__main__":
    main()
