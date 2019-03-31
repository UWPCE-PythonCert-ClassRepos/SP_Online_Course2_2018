"""
test code for donor_models.py

"""
import numpy as np
import pytest
from great_circle_v2 import great_circle

def test_great_circle():
    result = great_circle(-72.345, 34.323, -61.823, 54.826)
    e = 2
    answer = 1504.4407 #miles
    assert np.abs(result - answer) < e

