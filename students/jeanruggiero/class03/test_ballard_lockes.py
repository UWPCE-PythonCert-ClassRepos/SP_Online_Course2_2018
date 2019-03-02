#!/usr/bin/env python3

from ballard_lockes import Locke
from ballard_lockes import BoatError
import pytest

small_locke = Locke(5)
large_locke = Locke(10)
boats = 8

def test_init():
    l = Locke(7)
    assert isinstance(l, Locke)
    assert l.capacity == 7

def test_str():
    l = Locke(7)
    assert l.__str__() == 'Locke(7)'

def test_enter(capsys):
    with Locke(7) as l:
        pass
    out, err = capsys.readouterr()
    assert out == "\nEntering Locke(7)\n" +\
        "Restarting the pumps.\nOpening the doors.\nClosing the doors.\n" + \
        "Restarting the pumps.\n\nExiting Locke(7)\nRestarting the pumps.\n" + \
        "Opening the doors.\nClosing the doors.\nRestarting the pumps.\n"

def test_exit():
    pass

def test_move_boats_through_error():
    l = Locke(7)
    with pytest.raises(BoatError):
        l.move_boats_through(10)

def test_move_boats_through(capsys):
    l = Locke(7)
    l.move_boats_through(5)
    out, err = capsys.readouterr()
    assert out == '\nMoving 5 boats through Locke(7).\n'
