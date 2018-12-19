"""
test code for recursive_factorial.py

"""

import pytest
from recursive_factorial import factorial
import math

def test_factorial():
    assert factorial(5) == 120
    assert factorial(1) == 1
    assert factorial(4) == 24
    assert factorial(52) == math.factorial(52)
    assert factorial(0) == 1
    assert factorial(-32132) == 1