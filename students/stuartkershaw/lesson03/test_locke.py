import pytest

from locke import Locke


def test_locke_init():
    with pytest.raises(Exception) as excinfo:
        locke = Locke()

    assert str(excinfo.value) == "__init__() missing 1 required positional "\
                                 "argument: 'limit'"

    locke = Locke(5)

    assert locke.limit == 5


def test_small_locke():
    small_locke = Locke(5)

    assert small_locke.size == "SMALL LOCKE"


def test_large_locke():
    small_locke = Locke(10)

    assert small_locke.size == "LARGE LOCKE"


def test_boats():
    locke = Locke(5)
    locke.move_boats_through(5)

    assert locke.boats == 5


def test_entry_conditions():
    locke = Locke(5)
    locke.move_boats_through(5)

    assert locke.check_entry_conditions() is True

    with pytest.raises(ValueError) as excinfo:
        locke.move_boats_through(15)

    assert str(excinfo.value) == "LARGE LOCKE appects 10 boats max."
