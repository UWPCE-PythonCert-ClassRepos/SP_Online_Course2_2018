"""
test program for recursive_fix.py
"""

import pytest
from recursive_fix import *

def test_my_fun():
    assert my_fun(2) == True
    assert my_fun(64) == True
    assert my_fun(2048) == True
    assert my_fun(3) == False
    assert my_fun(15) == False
    assert my_fun(222) == False
