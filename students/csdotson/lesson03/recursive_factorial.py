#!/usr/bin/env python
""" Recursive solution for the factorial function """

def factorial(num):
    if num == 1:
        return(num)
    else:
        return num * factorial(num - 1)
        