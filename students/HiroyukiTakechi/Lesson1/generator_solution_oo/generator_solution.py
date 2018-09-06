'''
Lesson 1 Generator Draft 1
'''


def intsum():
    x = 0
    while True:
        yield x
        x += x+1 #this is not right.... I need to think a little more.


def doubler():
    [x*2 for x in range (0, 100)]


def fib(n):
    a = 0
    b = 1
    while True:
        a, b = b, a+b
        yield a

    
def prime():
    while True:
        for i in range(2,x):
            if x%i == 0:
                break
            else:
                yield x
            x += 1