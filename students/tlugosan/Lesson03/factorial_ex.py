#!/usr/bin/env python3

import pytest


def fact(input_number):
    """Computes recursively factorial numbers."""
    if input_number == 1:
        return input_number
    return input_number * fact(input_number - 1)


if __name__ == '__main__':
    """Test suite to verify FACTORIAL implementation."""

def test_1():
    assert fact(1) == 1

def test_2():
    assert fact(2) == 2


def test_3():
    assert fact(3) == 6


def test_4():
    assert fact(4) == 24

def test_7():
    assert fact(7) == 24*5*6*7
