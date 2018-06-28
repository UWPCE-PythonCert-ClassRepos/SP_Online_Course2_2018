#!/usr/bin/env python3


def factorial(number):
    if number > 1:
        return number * factorial(number - 1)
    else:
        return 1

if __name__ == '__main__':
    assert [factorial(x) for x in range(1, 11)] == [
            1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800]
    
    def output(number):
        print('The factorial of {} is {}.'.format(number, factorial(number)))
    
    output(5)
    output(7)
    output(10)
    output(3)
    output(6)
    output(2)
    output(0)
    output(4)
    output(1)
    output(9)
    output(8)