#!/usr/bin/env python
# Lesson1  - Aurel Perianu

"""
     example generators
"""
def intsum():
    """
        generator integes sum
    """
    tot = 0
    x = 0
    while True:
        #print (x)
        yield tot
        x += 1
        tot += x

def doubler():
    """
        each value is double the previous value
    """
    x = 1
    while True:
        yield x
        x *= 2

def fib():
    """
        Fibonacci Sequence
        f(n) = f(n-1) + f(n-2)
    """
    x, y = 1, 1
    while True:
        yield x
        #print (x)
        x, y = y, x + y

def prime():
    """
        prime number generator
    """
    num = 2
    while True:
        isprime = True
        for x in range(2, int(num**0.5 + 1)):
            if num % x == 0:
                isprime = False
                break
        if isprime:
            yield num
            #print(num)
        num += 1


if __name__ == "__main__":

    g = prime()
    for val in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43,
                47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]:
        assert next(g) == val
