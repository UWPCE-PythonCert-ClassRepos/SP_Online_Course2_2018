#!/usr/bin/env python 3

"""
Write a few generators:
Sum of integers
Doubler
Fibonacci sequence
Prime numbers
"""

"""
Descriptions:

Sum of the integers:
keep adding the next integer

0 + 1 + 2 + 3 + 4 + 5 = 0, 1, 3, 6, 10, 15 
"""
def intsum():
    number = 0
    sum = 0
    while True:
        sum += number
        yield sum
        number += 1

def intsum2():
    number = 0
    sum = 0
    while True:
        sum += number
        yield sum
        number += 1

"""
Doubler:
1, 2, 4, 8, 16, 32,
"""
def doubler():
    '''Each value is double the previous value:'''
    start = 1
    while True:
        yield start
        start *= 2


"""
Fibonacci sequence:
The Fibonacci sequence as a generator:
f(n) = f(n-1) + f(n-2)
1, 1, 2, 3, 5, 8, 13, 21, 34…
"""
def fib():
    '''without the 0 at the beginning of the sequence'''
    num1, num2 = 1,1
    while True:
        yield num1
        num1, num2 = num2, num1 + num2

def fib1():
    '''Fib sequence with the 0 at the begginning'''
    num1, num2 = 0, 1
    while True:
        yield num1
        num1, num2 = num2, num1 + num2
"""
Prime numbers:
2, 3, 5, 7, 11, 13, 17, 19, 23…
"""
def prime():
    '''Generate the prime numbers (numbers only divisible by them self and 1)'''
    num = 2
    while True:
        if num < 2 or not [a for a in range(2, num) if num % a == 0]:
            yield num
        num +=1
