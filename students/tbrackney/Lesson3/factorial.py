"""
File Name: factorial.py
Author: Travis Brackney
Class: Python 220 - Self paced online
Date Created 2/3/2019
Python Version: 3.6.4
"""

def factorial(n):
    if n == 1:
        return 1
    return n * factorial(n-1)
