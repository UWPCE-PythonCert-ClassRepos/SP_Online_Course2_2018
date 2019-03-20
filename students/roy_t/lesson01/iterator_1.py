#!/usr/bin/env python3

__author__ = "roy_t githubtater"


def IterateMe_2(start, stop, step=1):
    """Simple generator that iterates from start to stop, incrementing by step"""
    for x in range(stop // step):
        # verify we have valid values to start with
        if start >= stop:
            break
        else:
            yield start
            start += step


def main():
    it = IterateMe_2(2, 20, 2)
    ## commenting out the code below in order to behave more like range()
    # for i in it:
    #     if i > 10:  break
    #     print(i)
    for i in it:
        print(i)


if __name__ == "__main__":
    main()
