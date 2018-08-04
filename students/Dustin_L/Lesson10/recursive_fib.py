#!/usr/bin/env python3
import sys


def fib(n):
    """Recursively computes the fibonacci value to the 'nth' level.

    Args:
        n (int): Fibonacci level, must be greater than or equal to 0.

    Raises:
        ValueError: Raised if n is less than 0.

    Returns:
        int: Fibonacci result
    """
    if n in (0, 1):
        return n
    if n < 0:
        raise ValueError("'n' must be greater than or equal to 0")

    return fib(n - 2) + fib(n - 1)


def main():
    """Main function"""
    if len(sys.argv) > 1:
        try:
            in_val = int(sys.argv[1])
        except ValueError:
            print('Must pass in an integer value')
        else:
            if in_val >= 0:
                print(fib(in_val))
            else:
                print('Must pass in a value greater than or equal to 0')


if __name__ == '__main__':
    main()
