import math
# Sum of integers
def intsum(curr_int=0, next_add=1):
    while True:
        yield curr_int
        curr_int += next_add
        next_add += 1


def intsum2(curr_int=0, next_add=1):
    while True:
        yield curr_int
        curr_int += next_add
        next_add += 1


# Doubler
def doubler(curr_int=1):
    while True:
        yield curr_int
        curr_int = curr_int*2


# Fibonacci sequence
def fib():
    nm2_int = 0
    nm1_int = 1
    while True:
        yield nm1_int
        temp = nm2_int
        nm2_int = nm1_int
        nm1_int += temp


# Prime numbers
def prime():
    val = 2
    while True:
        prime = True
        for i in range(2, int(math.sqrt(val))+1):
            if val % i == 0:
                prime = False
        if prime is True:
            yield val
        val += 1
