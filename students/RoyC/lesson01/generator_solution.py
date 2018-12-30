#!/usr/bin/env python3
# Lesson 01, Generators

def intsum():
    """
    Generator for contnuously summing ints
    """
    rtnval = 0
    i = 1
    while True:
        yield rtnval
        rtnval = rtnval + i
        i += 1
        
def intsum2():
    """
    This method is in test_generator but not instructions, so just copying intsum
    """
    rtnval = 0
    i = 1
    while True:
        yield rtnval
        rtnval = rtnval + i
        i += 1
        
def doubler():
    """
    Generator that doubles the previous value
    """
    rtnval = 1
    while True:
        yield rtnval
        rtnval *= 2

def fib():
    """
    Generator for fibonacci series
    """
    rtnval = 1;
    val0 = 0
    val1 = 1
    while True:
        yield rtnval
        rtnval = val0 + val1
        val0 = val1
        val1 = rtnval
    
def prime():
    """
    Generator for prime numbers
    """
    rtnval = 2
    while True:
        if not [x for x in range(2, rtnval) if rtnval % x == 0]:
            yield rtnval
        rtnval += 1