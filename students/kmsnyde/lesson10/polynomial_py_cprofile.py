# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 15:00:02 2018

@author: HP-Home
"""
import cProfile


# Find the root of a polynomial

def f(x):
    func = (x**3) - (x * 2) -1
    return func

def derivative(x):
    h = 0.000001
    derivative = (f(x + h) - f(x)) / h
    return derivative

def newton_raphson(x):
    return (x - (f(x)) / derivative(x))

# p: the initial point i.e. a value closer to the root
# n: number of iterations
    
def iterate(p, n):
    x = 0
    for i in range(n):
        if i == 0:
            x = newton_raphson(p)
        else:
            x = newton_raphson(iterate(x, n))
            
        n = n - 1
    return x

if __name__ == '__main__':
    
    print('"cProfile REPORT OUTPUT"')
    _sign = '=' * 80
    print(_sign)
    
    pr = cProfile.Profile()
    pr.enable()
    
    iterate(5, 17)
    
    pr.disable()
    pr.print_stats()
    
    print('"END REPORT"')
    print(_sign)