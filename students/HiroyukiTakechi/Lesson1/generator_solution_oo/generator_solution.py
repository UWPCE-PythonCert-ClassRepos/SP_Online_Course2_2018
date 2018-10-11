'''
Lesson 1 Generator Draft 1
'''


def intsum(x=0, total=0):

    while True:
        total += x
        yield total
        x += 1

def doubler(x=1):

    while True:
        yield x
        x *= 2

def fib(a=0, b=1):

    while True:
        a, b = b, a+b
        yield a

    
def prime(x=2):
    while True:
        for i in range(2,x):
            if x%i == 0:
                break
        else:
            yield x
        x += 1
