"""
test code for locke_manager.py

"""

import pytest
from locke_manager import Locke


def test_Locke():
    small_locke = Locke(5)
    large_locke = Locke(10)
    boats = 8
    with pytest.raises(ValueError):
        small_locke.move_boats_through(boats)
    with large_locke as locke:
        locke.move_boats_through(boats)
    assert True


def test_manager():
    small_locke = Locke(5)
    large_locke = Locke(10)
    boats = 8
    with large_locke as locke:
        assert not locke.pumps_on
        assert not locke.door_closed
    assert large_locke.pumps_on
    assert large_locke.door_closed
