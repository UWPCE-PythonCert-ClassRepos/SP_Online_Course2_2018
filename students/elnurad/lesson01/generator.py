#!/usr/bin/env python
def intsum():
    i = 0
    sum = 0
    while True:
        yield sum
        i += 1
        sum += i


def doubler():
    i = 1
    while True:
        yield i
        i *= 2


def fib():
    i, j = 1, 1
    while True:
        yield i
        i, j = j, i+j 
   
    
def is_prime(i):
    for x in range(2,i):
        if i%x == 0:
            return False
    return True
   
       
def prime():
    i = 2
    while True:
        if is_prime(i):
            yield i
        i+=1




            


    
