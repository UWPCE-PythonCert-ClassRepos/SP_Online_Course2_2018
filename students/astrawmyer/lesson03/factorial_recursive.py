#!/usr/bin/env python

def factorial(n):
    result = n * factorial(n-1)
    return result

print(factorial(3))