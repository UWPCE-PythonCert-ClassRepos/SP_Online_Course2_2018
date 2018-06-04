#!/usr/bin/env python3
"""Recursive Factorial Module"""


def recursive_factorial(n):
    """Computes factorial of n recursively.

    Args:
        n (int): Level of factorial

    Returns:
        int: factorial of n
    """
    if not n or n == 1:
        return 1

    return n * recursive_factorial(n - 1)


def main():
    """Main function"""
    print(recursive_factorial(5))


if __name__ == '__main__':
    main()
