#!/usr/bin/env python3
# Ian Letourneau
# 7/6/2018

import generator as g

# Test Sum of Integers generator


def test_sum_of_int():
    gen = g.sum_of_int(47)
    for i in gen:
        print(i)

# Test Doubler generator


def test_doubler():
    gen2 = g.doubler(47)
    for i in gen2:
        print(i)

# Test Fibonacci generator


def test_fib():
    gen3 = g.fib(47)
    for i in gen3:
        print(i)

# Test Prime Number generator


def test_prime():
    gen4 = g.prime(47)
    for i in gen4:
        print(i)
