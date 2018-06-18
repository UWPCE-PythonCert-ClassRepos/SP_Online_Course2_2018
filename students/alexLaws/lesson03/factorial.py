#!/usr/bin/env python3


def factorial(num):
    if num < 0:
        print('You tried factorial of {}. '
              'Factorials do not work for negative numbers!'.format(num))
    elif num == 1 or num == 0:
        return 1
    else:
        return num * factorial(num - 1)


factorial(-5)
print('The factorial of 0 is {:,}'.format(factorial(0)))
print('The factorial of 2 is {:,}'.format(factorial(2)))
print('The factorial of 3 is {:,}'.format(factorial(3)))
print('The factorial of 4 is {:,}'.format(factorial(4)))
print('The factorial of 5 is {:,}'.format(factorial(5)))
print('The factorial of 6 is {:,}'.format(factorial(6)))
print('The factorial of 17 is {:,}'.format(factorial(17)))
