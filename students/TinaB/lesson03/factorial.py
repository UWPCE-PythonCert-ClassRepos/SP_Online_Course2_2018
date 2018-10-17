#!/usr/bin/env python3

# Lesson 03 - Recursive Factorial

"""
Write a recursive solution for the factorial function.
https://en.wikipedia.org/wiki/FactorialLinks to an external site.
"""

def factorial(n):
    if n < 1: # handles the first call of 0
        return 1
    else:
        facttotal = n * factorial(n-1) #recursive call
        print(f'{n}! = {facttotal}')
        return facttotal
