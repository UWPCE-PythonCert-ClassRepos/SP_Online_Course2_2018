#!/usr/bin/env python3
"""
File Name: generator.py
Author: Travis Brackney
Class: Python 220 - Self paced online
Date Created 1/14/2019
Python Version: 3.6.4
"""


def sum_int():
    i = 0
    x = i
    while True:
        x += i
        i += 1
        yield x


def doubler():
    i = 1
    while True:
        yield i
        i *= 2


def fibonacci():
    min1 = 0
    min2 = 0
    while True:
        sum = min1 + min2
        yield sum
        if sum == 0:
            min1 = 1
        min2 = min1
        min1 = sum
