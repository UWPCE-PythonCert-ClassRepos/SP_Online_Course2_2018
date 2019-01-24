#!/usr/bin/env python3


__author__ = 'roy_t'


# this function was 'borrowed' from the following text:
# Lott, S. (2015) Chapter 6. Recursions and Reductions. In Functional Python Programming.
def factorial(n):
    """Return the factorial of n"""
    if n == 0: return 1
    # otherwise: recurse through the function until the final call, n*1, stopping the recursion.
    else: return n*factorial(n-1)


def factorial_report(n, fac):
    """Print a report of factorials and their values"""
    format_str = '{:>5}! = {:<10}'
    print(format_str.format(n, fac))


def main():

    # begin by printing a title
    title = ' Factorials '
    print('\n{:*^20}'.format(title))

    # start the loop and print the resulting factorial
    for i in range(10):
        factorial_report(i, factorial(i))


if __name__ == '__main__':
    main()