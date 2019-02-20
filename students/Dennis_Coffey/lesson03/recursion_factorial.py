# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 20:15:22 2019

@author: dennis
"""

""" Recursion function to generate a factorial """
def factorial(end_point):
    if end_point == 0 or end_point == 1:
        return 1
    return end_point * factorial(end_point - 1)
    
# Test factorial function for different values    
assert factorial(0) == 1
assert factorial(1) == 1
assert factorial(4) == 24
assert factorial(6) == 720