

def int_sum(n=0, next_num=0):
    while True:
        next_num += n
        yield next_num
        n += 1


def doubler(n=1,double_num=1):
    while True:
        double_num = n
        yield double_num
        n *= 2


def fib(n1=0,n2=1):
    while True:
        fib_series = n2
        yield fib_series
        fib_series = n1 + n2
        n1 = n2
        n2 = fib_series

