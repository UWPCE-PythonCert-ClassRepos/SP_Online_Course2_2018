#!/usr/bin/env python
from recursion import factorial
import pytest

def test_factorial():
    assert factorial(5) == 120
    assert factorial(7) == 5040
    assert factorial(4) == 24
