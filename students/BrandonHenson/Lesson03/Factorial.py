# Brandon Henson
# Python 220
# Lesson 3 Factorial
# 7-6-18
# !/usr/bin/env python3


def factorial(number):
    if number > 1:
        return number * factorial(number - 1)
    else:
        return 1

if __name__ == '__main__':
    factorial(5)
    for i in range(0, 20):
        print(i, "=", factorial(i))
