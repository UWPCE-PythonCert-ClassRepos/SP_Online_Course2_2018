#!/usr/bin/env python3

def sum():
    num = 0
    total = 0
    while True:
        total += num
        yield total
        num += 1

def doubler():
    total = 1
    while True:
        yield total
        total *= 2
     

def fibonacci():
    num = 0
    next = 1
    while True:
        yield next
        num, next = next, num + next
        print(next)
    

def prime():
    num = 2
    while True:
        if not [x for x in range(2, num) if num % x ==0]:
            yield num
        num += 1



