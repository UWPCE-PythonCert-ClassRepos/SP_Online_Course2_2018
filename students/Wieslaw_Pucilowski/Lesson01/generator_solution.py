__author__="Wieslaw Pucilowski"

def intsum():
    i, sum = 0, 0
    while True:
        sum += i
        yield sum
        i += 1

def intsum2():
    i, sum = 0, 0
    while True:
        sum += i
        yield sum
        i += 1
def doubler():
    i = 1
    while True:
        yield i
        i = i * 2

def fib():
    x, y = 0, 1
    while True:
        x, y = y, x + y
        yield x

def prime():
    i = 2
    while True:
        if not [x for x in range(2, i) if i % x == 0]:
            yield i
        i += 1