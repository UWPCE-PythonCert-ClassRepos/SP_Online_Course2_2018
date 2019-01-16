"""
Lesson 10 Assignment - Memory Profiler on Lesson 3 recursion
"""

from memory_profiler import profile


@profile
def fact(n):
    if n <= 1:
        return 1
    return n * fact(n - 1)


def main():
    fact(5)


if __name__ == '__main__':
    main()