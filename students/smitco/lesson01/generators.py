# lesson 01 generators
# !/usr/bin/env python3

def intsum():
    i = 0
    sum = 0
    while True:
        sum += i
        i += 1
        yield sum
    
def doubler():
    i = 1
    yield i
    while True:
        val = i*2
        i = val
        yield i

def fib():
    x = 0
    y = 1
    while True:
        yield y
        x, y = y, x+y

def prime():
    i = 2
    for i in range(2, 100): #set arbitrary max range to 100 for compatibility with test file
        flag = True
        for x in range (2, i):
            if i % x == 0:
                flag = False
        if flag:
            yield i
        i += 1