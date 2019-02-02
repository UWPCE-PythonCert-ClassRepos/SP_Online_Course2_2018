"""tests the behavior of the locke system"""

import pytest
import locke


def test_locke_accepts_boats_count_under_limit():
    """given a lock established with a boat limit of 5
    when 5 or less boats are input
    the locke works without exception"""
    assert 1==2

def test_locke_rejects_boats_count_over_limit():
    """given a lock established with a boat limit of 5
    when more than limit of boats are input
    the locke raises input error exception"""
    assert 1==2

def test_locke_errors_on_bad_inputs():
    """given inputs other than positive ints or 0
    the locke sends inputerror on initialization"""
    assert 1==2