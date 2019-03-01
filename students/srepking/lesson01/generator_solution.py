

def intsum():
    startval = 0
    while True:
        yield startval
        startval += 1


def intsum2():
    start_val1 = 0
    int_gen = intsum()
    while True:
        next_int = next(int_gen)
        yield start_val1+next_int
        start_val1 = start_val1+next_int


def doubler():
    start_val1 = 1
    while True:
        yield start_val1
        start_val1 = start_val1 * 2


def fib():
    start_val1 = 1
    start_val2 = 1
    yield 1
    yield 1
    while True:
        next_num = start_val1 + start_val2
        yield next_num
        start_val1 = start_val2
        start_val2 = next_num


def prime():
    num_gen = intsum()
    next_num = next(num_gen)
    while next_num < 2:
        next_num = next(num_gen)
    yield 2
    next_num = next(num_gen)
    while True:
        for i in range(2, next_num):
            if (next_num % i) == 0:
                next_num = next(num_gen)
                break
        else:
            yield next_num
            next_num = next(num_gen)





