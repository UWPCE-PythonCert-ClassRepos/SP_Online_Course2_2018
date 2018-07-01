# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 17:18:15 2018

@author: Karl M. Snyder
"""

# recursive function for factorials
def factorial(x):
    if x == 0: return 1
    return x * factorial(x-1)

if __name__ == "__main__":
    for x in range(1, 11):
        print("factorial for,",x, "is ", factorial(x))