import io
import pytest

from Context_Managers import *

def test_lock_size():
    a = Locke(55)
    assert a.size == 55
    
def test_multiple_lock_size():
    a = Locke(10)
    b = Locke(5)
    assert a.size == 10
    assert b.size == 5
    
def test_initialization(capsys):
    a = Locke(5)
    captured = capsys.readouterr()
    expected = 'Initializing lock system...\n'
    assert captured.out == expected

def test_big_locke(capsys):
    a = Locke(10)
    boats = 8
    with a as locke:
        locke.move_boats_through(boats)
    captured = capsys.readouterr()
    expected = 'Initializing lock system...\nStopping the pumps\nOpening the doors\n\
Closing the doors\nRestarting the pumps\n8 boats have entered!\nStopping the pumps\n\
Opening the doors\nClosing the doors\nRestarting the pumps\n8 boats have exited!\n'
    assert captured.out == expected
    
def test_small_locke(capsys):
    a = Locke(10)
    boats = 12
    try:
        with a as locke:
            locke.move_boats_through(boats)
    except RuntimeError:
#this checks that the RuntimeError is raised, and allows it to pass to complete this test
        pass
    captured = capsys.readouterr()
    expected = 'Initializing lock system...\nPlease reduce number of boats.\n'
    assert captured.out == expected
    
def test_multiple_lockes(capsys):
    a = Locke(10)
    b = Locke(15)
    boats = 8
    with a as locke:
        locke.move_boats_through(boats)
    captured = capsys.readouterr()
    expected = 'Initializing lock system...\nInitializing lock system...\nStopping the pumps\nOpening the doors\n\
Closing the doors\nRestarting the pumps\n8 boats have entered!\nStopping the pumps\n\
Opening the doors\nClosing the doors\nRestarting the pumps\n8 boats have exited!\n'
    assert captured.out == expected
    with b as locke:
        locke.move_boats_through(boats)
    captured = capsys.readouterr()
    expected = 'Stopping the pumps\nOpening the doors\n\
Closing the doors\nRestarting the pumps\n8 boats have entered!\nStopping the pumps\n\
Opening the doors\nClosing the doors\nRestarting the pumps\n8 boats have exited!\n'
    assert captured.out == expected
    
