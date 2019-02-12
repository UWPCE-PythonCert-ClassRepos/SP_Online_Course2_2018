# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 20:46:46 2019

@author: dennis
"""
"""Generator to produce sum of integers, doubler, fibonacci series, and prime numbers"""

# Generator to sum integer list - used simple but limiting for statement
def intsum():
    sumtotal = 0
    for i in range(40):
        sumtotal += i
        yield sumtotal

# Generator to sum integer list - used while True to allow infinite generation
def intsum2():
    sumtotal = 0
    i = 0
    while True:
        sumtotal += i
        yield sumtotal
        i += 1

# Generator to output double from integer list
def doubler():
    value = 1
    while True:
        yield value
        value *= 2
        
# Generator to output fibonacci series
def fib():
    prior = 0
    current = 1
    while True:
        yield current
        temp = current
        current += prior
        prior = temp
        
# Generator to output prime numbers
def prime():
    divlist = [2,3,5,7,9]
    for i in range(2,200):
        prime = True
        for div in divlist:
            if i%div == 0 and i != div:
                prime = False
        if prime == True:
            yield i
            if i > 9:
                divlist.append(i)

# Generator to output squares
def square():
    i = 0
    while True:
        yield i ** 2
        i += 1

# Generator to output cubes
def cube():
    i = 0
    while True:
        yield i ** 3
        i += 1

# Generator to count by threes
def countby3():
    i = 1
    while True:
        if i%3 == 0:
            yield i
        i += 1

# Output of intsum or intsum2
g = intsum2()
i = 0
print("Integer sum")
while i<6:
    print(next(g))
    i += 1
    
# Output of doubler
g = doubler()
i = 0
print("Doubler")
while i<6:
    print(next(g))
    i += 1

# Output of fibonacci series
g = fib()
i = 0
print("Fibonacci series")
while i<6:
    print(next(g))
    i += 1

# Output of prime numbers
g = prime()
i = 0
print("Prime numbers")
while i<25:
    print(next(g))
    i += 1

# Output of square
g = square()
i = 0
print("Square")
while i<6:
    print(next(g))
    i += 1

# Output of cube
g = cube()
i = 0
print("Cube")
while i<6:
    print(next(g))
    i += 1

# Output counting by 3
g = countby3()
i = 0
print("Count by three")
while i<6:
    print(next(g))
    i += 1
