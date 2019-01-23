#!/usr/bin/env python
"""test suite for the iterator.py example"""

from iterator_1 import IterateMe_1

def test_iterate_matches_range():
    """tests the IterateMe matches range
    when forced to list"""
    assert list(range(4)) == list(IterateMe_1(4))

