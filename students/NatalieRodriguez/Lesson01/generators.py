#!/usr/bin/env python 3

#Natalie Rodriguez
#UW Python - Course 2
#Lesson 1: Generators
#June 28, 2018

#Sum of Integers
# (ex: 0+1+2+3+4 etc = 0, 1, 3, 6, 10)

def sum_ints():
    int = 0
    sum = 0
    while True:
        sum += int
        int += 1
        yield sum

#Doubler
#Double the previous value: 1, 2, 4, 8, 16, 32

def doubler():
    x = 1
    while True:
        yield x
        x *= 2

#Fibonacci Sequence
#f(n) = f(n-1)+f(n-2)
#1, 1, 2, 3, 5, 8, 13, 21, 34

def fibonacci():

    x = 0
    y = 1
    while True:
        yield y
        x, y = y, x + y

#Prime Numbers
#only divisible by self and 1.
#2, 3, 5, 7, 11, 13, 17, 19, 23

def primes():

    y = 2
    while True:
        if not [x for x in range(2, y) if y % x == 0]:
            yield y
        y+=1

#Squares

def squared():
    x = 1
    while True:
        yield x * x
        x += 1

#Cubes

def cubed():
    x = 1
    while True:
        yield x * x * x
        x += 1