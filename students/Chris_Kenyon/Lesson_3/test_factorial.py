#!/usr/bin/env python3
# Lesson 3: Test Recursive Factorial

# !/usr/bin/env python3
# Lesson 3:Test Recursive Factorial

from factorial import factorial


def tests():
    assert factorial(1) == 1
    assert factorial(2) == 2
    assert factorial(3) == 6
    assert factorial(4) == 24
    assert factorial(5) == 120
    assert factorial(6) == 720
    assert factorial(13) == 6227020800
    assert factorial(19) == 121645100408832000
