#!/usr/bin/env python
""" A series of simple generators """

def sum_of_integers(a=0):
    count = a
    while True:
        yield(a)
        count += 1
        a += count


def doubler():
    pass


def fib_sequence():
    pass 


def prime_numbers():
    pass 


