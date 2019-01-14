#!/usr/bin/env python3
#Lesson 3, Recursive factorial function

def factorial(n):
    """
    Compute factorial of given number
    Only valid for positive numbers greater than zero; recursively multiplies the
    value by the preceding integer, down to 1
    """
    if n < 1:
        raise ValueError("Not a valid value, must be greater than zero")
    elif n == 1:
        return 1
    else:
        return n * factorial(n-1)

if __name__ == '__main__':
    # tests function for some random values
    assert(factorial(1) == 1)
    assert(factorial(2) == 2)
    assert(factorial(6) == 720)
    assert(factorial(9) == 362880)
    assert(factorial(13) == 6227020800)