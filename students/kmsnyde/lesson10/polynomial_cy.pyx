# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 15:00:02 2018

@author: HP-Home
"""

# Find the root of a polynomial

cpdef double f( double x):
    cdef double func = (x**3) - (x * 2) -1
    return func

cpdef double derivative(double x):
    cdef double h = 0.000001
    cdef double derivative = (f(x + h) - f(x)) / h
    return derivative

cpdef newton_raphson(double x):
    return (x - (f(x)) / derivative(x))

# p: the initial point i.e. a value closer to the root
# n: number of iterations
    
cpdef iterate(int p, int n):
    cdef int x = 0
    cdef int i
    for i in range(n):
        if i == 0:
           x = newton_raphson(p)
        else:
           x = newton_raphson(iterate(x, n))
        n = n - 1
    return x