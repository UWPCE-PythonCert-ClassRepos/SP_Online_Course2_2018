def sum_generator():
    i = 0
    sum = 0
    while True:
        sum = sum + i
        yield sum
        i += 1

def double_generator():
    i = 1
    while True:
        yield i
        i = i*2

def fibonacci_generator():
    a = 0
    b = 1
    sum = 0
    while True:
        yield a
        sum = a + b
        a = b
        b = sum

def prime_generator():
    a = 2
    while True:
        if not [x for x in range(2,a) if a % x == 0]:
            yield a
        a = a + 1