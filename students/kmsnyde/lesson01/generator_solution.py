# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 09:09:02 2018

@author: Karl M. Snyder
"""

import itertools
import operator

def intsum(stop=100):
    ints = list(range(stop))
    return (itertools.accumulate(ints, operator.add))

def intsum2(stop=100):
    ints = list(range(stop))
    return (itertools.accumulate(ints, operator.add))

def doubler(start=1):
    # create a generator loop starting at 1 and doubling value af
    # start each time next() is called
    while True:
        yield start
        start *= 2
        
def fib(a=1, b=1):
    while True:
        yield a
        a, b = b, a + b
    
def prime(start=2):
    # had to research to figure this out in my own way
    while True:
        if start < 2 or not [x for x in range(2, start) if start % x == 0]:
             yield start        
        start += 1    
    

if __name__ == '__main__':
    a = intsum()
    assert next(a) == 0
    assert next(a) == 1
    
    b = doubler()
    assert next(b) == 1
    assert next(b) == 2
    assert next(b) == 4
    
    c = fib()
    assert next(c) == 1
    assert next(c) == 1
    assert next(c) == 2
    assert next(c) == 3
    assert next(c) == 5
    
    d = prime()
    assert next(d) == 2
    assert next(d) == 3
    assert next(d) == 5
    assert next(d) == 7
    

        

