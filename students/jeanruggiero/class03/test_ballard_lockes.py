#!/usr/bin/env python3

from ballard_lockes import Locke
import pytest

small_locke = Locke(5)
large_locke = Locke(10)
boats = 8
#
# with small_locke as locke:
#     locke.move_boats_through(boats)
#
# with large_locke as locke:
#     locke.move_boats_through(boats)

def test_init():
    l = Locke(7)
    assert isinstance(l, Locke)
    assert l.capacity == 7

def test_str():
    l = Locke(7)
    assert l.__str__() == 'Locke(7)'

def test_enter():
    with Locke(7) as l:
        pass

    captured = capsys.readouterr()
    assert captured.out == "Restarting the pumps.\nRestarting the pumps." + \
        "\nOpening the doors.\nClosing the doors."

def test_exit():
    pass

def test_move_boats_through():
    l = Locke(7)
    with pytest.raises(ValueError):
        l.move_boats_through(10)

    l.move_boats_through(5)
    captured = capsys.readouterr()
    assert captured.out == '\nMoving boats through Locke(7).'


# def __enter__(self):
#     print("\nEntering locke {}".format(self))
#     self.stop_pumps()
#     self.open_doors()
#     self.close_doors()
#     self.start_pumps()
#     return self
#
# def __exit__(self, type, value, traceback):
#     print("\nExiting locke {}".format(self))
#     self.stop_pumps()
#     self.open_doors()
#     self.close_doors()
#     self.start_pumps()
#
#     if type:
#         return False
