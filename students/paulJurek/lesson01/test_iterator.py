#!/usr/bin/env python
"""test suite for the iterator.py example"""

from iterator_1 import IterateMe_1, IterateMe_2

def test_iterate_matches_range():
    """tests the IterateMe matches range
    when forced to list"""
    assert list(range(4)) == list(IterateMe_1(4))

def test_iterate2_matches_range():
    """tests the IterateMe matches range
    when forced to list"""
    assert list(range(4)) == list(IterateMe_2(0,4,1))

def test_iterateme_behavior_matches_range():
    """given a start, stop, step input
    when iterateme is run, interrupted and then restarted
    and so is range
    both produce same outputs"""
    START = 2
    END = 20
    STEP = 2
    it = IterateMe_2(START, END, STEP)
    ran = range(START,END,STEP)

    # run iterate me results
    it_results = []
    for i in it:
        if i > 10:  break
        it_results.append(i)
    for i in it:
        it_results.append(i)

    # run range results
    ran_results= []
    for i in ran:
        if i > 10:  break
        ran_results.append(i)
    for i in ran:
        ran_results.append(i)
    
    assert it_results == ran_results