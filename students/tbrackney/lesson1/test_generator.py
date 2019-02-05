#!/usr/bin/env python3
"""
File Name: test_generator.py
Author: Travis Brackney
Class: Python 220 - Self paced online
Date Created 1/14/2019
Python Version: 3.6.4
"""


import generator as gen


def test_sum_int():
    i = gen.sum_int()
    assert next(i) == 0
    assert next(i) == 1
    assert next(i) == 3
    assert next(i) == 6
    assert next(i) == 10


def test_doubler():
    d = gen.doubler()
    assert next(d) == 1
    assert next(d) == 2
    assert next(d) == 4
    assert next(d) == 8
    assert next(d) == 16
    assert next(d) == 32


def test_fibonacci():
    i = gen.fibonacci()
    assert next(i) == 0
    assert next(i) == 1
    assert next(i) == 1
    assert next(i) == 2
    assert next(i) == 3
    assert next(i) == 5
    assert next(i) == 8
    assert next(i) == 13
    assert next(i) == 21
    assert next(i) == 34
