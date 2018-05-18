#!/usr/bin/env python3

def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return factorial(n-1) * n

for i in range(0,31):
    print('Factorial({}) = {}'.format(i, factorial(i)))
