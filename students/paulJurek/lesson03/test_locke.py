"""tests the behavior of the locke system"""

import pytest
import sys
from locke import Locke


def test_locke_accepts_boats_count_under_limit():
    """given a lock established with a boat limit of 5
    when 5 or less boats are input
    the locke works without exception"""
    locke1 = Locke(5)
    boats = 4
    print(locke1.__dict__)
    with locke1:
        print(locke1.__dict__)
        assert locke1.move_boats_through(boats)

def test_locke_rejects_boats_count_over_limit():
    """given a lock established with a boat limit of 5
    when more than limit of boats are input
    the locke raises value error exception"""
    locke1 = Locke(5)
    boats = 6
    with pytest.raises(ValueError):
        with locke1:
            locke1.move_boats_through(boats)


@pytest.mark.parametrize("bad_input", [
    (-1),
    (1.2),
    (0.123),
])
def test_locke_errors_on_bad_inputs(bad_input):
    """given inputs other than positive ints or 0
    the locke sends inputerror on initialization"""
    locke1 = Locke(5)
    boats = bad_input
    with pytest.raises(ValueError):
        with locke1:
            locke1.move_boats_through(boats)

def test_locke_typeerrors_on_str_inputs():
    """given inputs other than positive ints or 0
    the locke sends inputerror on initialization"""
    locke1 = Locke(5)
    boats = 'hello'
    with pytest.raises(TypeError):
        with locke1:
            locke1.move_boats_through(boats)

def test_std_output_tells_story(capsys):
    """given a locke
    when moving boats through
    the standard output tells steps"""
    locke1 = Locke(5)
    boats = 4
    with locke1:
        locke1.move_boats_through(boats)
    captured = capsys.readouterr().out.split("\n")
    assert captured[0] == "run pumps"
    assert captured[1] == "open door1"
    assert captured[2] == "moving boats"
    assert captured[3] == "closing door1"
    assert captured[4] == "starting pumps"
    assert captured[5] == "moving 4 boats through locks"
    assert captured[6] == "open door 2"
    assert captured[7] == "moving boats"
    assert captured[8] == "closing door 2"

