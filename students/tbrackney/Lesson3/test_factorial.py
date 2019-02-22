"""
File Name: factorial.py
Author: Travis Brackney
Class: Python 220 - Self paced online
Date Created 2/3/2019
Python Version: 3.6.4
"""
import factorial as f

def test_factorial():
    assert f.factorial(1) == 1
    assert f.factorial(2) == 2
    assert f.factorial(5) == 120
    assert f.factorial(10) == 3628800
