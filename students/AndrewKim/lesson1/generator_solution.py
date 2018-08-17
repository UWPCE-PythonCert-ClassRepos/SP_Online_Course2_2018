#!/usr/bin/env python3

def intsum():
    i = 0
    sum = 0;
    while True:
        sum += i
        yield sum
        i += 1

def intsum2():
    i = 1
    sum = 0;
    while True:
        yield sum
        sum += i
        i += 1

def doubler():
    i = 1
    while True:
        yield i
        i *= 2
        
def fib():
    i = 0
    j = 1
    while True:
        yield j
        i , j = j , i+j
        
def prime():
    i=2
    while True:
        if i < 2 or not [x for x in range(2, i) if i % x == 0]:
            yield i
        i += 1
    