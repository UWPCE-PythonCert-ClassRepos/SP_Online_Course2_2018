# Author: Andy Kwok
# Last Updated: 10/23/18

def intsum(num=0):
    while True:
        if num == 0:
            sum = num
        else:
            sum += num
        yield sum
        num += 1

   
def intsum2(num=0):
    while True:
        if num == 0:
            sum = num
        else:
            sum += num
        yield sum
        num += 1


def doubler(double=1):
    while True:
        yield double
        double = 2 * double


def fib(fiblist=[]):
    while True:
        if len(fiblist) <= 1:
            fiblist += [1]
        else:
            fiblist += [fiblist[-1] + fiblist[-2]]
        yield fiblist[-1]


def prime(num=2):
    pri = 0
    while True:
        for i in range(2, num):
            if (num % i) == 0:
                pri = 0
                break
            else:
                pri = 1
        if pri == 1 or num == 2:
            print(num)
            yield num
        num += 1
