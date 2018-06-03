#!/usr/bin/env python


def intsum():
    """
    Adds next integer y to integer state x
    """
    x = 0
    y = 0
    while True:
        x += y
        y += 1
        yield x


def doubler():
    """
    Doubles the value of x
    """
    x = 1
    while True:
        yield x
        x = 2*x
