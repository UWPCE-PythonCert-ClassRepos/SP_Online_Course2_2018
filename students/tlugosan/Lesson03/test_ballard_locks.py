#!/usr/bin/env python3

import pytest
import ballard_locks as bl


def test_init():
    b1 = bl.Locke(10)


def test_init_fails():
    with pytest.raises(ValueError):
        b1 = bl.Locke(0)


def test_large_locke_few_boats(capsys):
    b1 = bl.Locke(10)
    boats_to_sail = 8
    b1.move_boats_through(boats_to_sail)
    captured = capsys.readouterr()
    out = captured.out.strip()
    prep_lock_before = "Stop pumps.\n" + "Opening doors.\n"
    prep_lock_after = "Closing doors.\n" + "Restarting pumps."
    assert out == prep_lock_before + "The boats have sailed through.\n" + prep_lock_after


def test_max_capacity_usage_locke(capsys):
    b1 = bl.Locke(10)
    boats_to_sail = 10
    b1.move_boats_through(boats_to_sail)
    captured = capsys.readouterr()
    out = captured.out.strip()
    prep_lock_before = "Stop pumps.\n" + "Opening doors.\n"
    prep_lock_after = "Closing doors.\n" + "Restarting pumps."
    assert out == prep_lock_before + "The boats have sailed through.\n" + prep_lock_after


def test_too_many_boats():
    b1 = bl.Locke(5)
    boats_to_sail = 8
    with pytest.raises(ValueError):
        b1.move_boats_through(boats_to_sail)


def test_no_boats(capsys):
    b1 = bl.Locke(5)
    boats_to_sail = 0
    b1.move_boats_through(boats_to_sail)
    captured = capsys.readouterr()
    out = captured.out.strip()
    prep_lock_before = "Stop pumps.\n" + "Opening doors.\n"
    prep_lock_after = "Closing doors.\n" + "Restarting pumps."
    assert out == prep_lock_before + "Testing the locke.\n" + prep_lock_after


def test_waiting_for_boats(capsys):
    b1 = bl.Locke(5)
    boats_to_sail = -1
    with pytest.raises(ValueError):
        b1.move_boats_through(boats_to_sail)
    assert 
