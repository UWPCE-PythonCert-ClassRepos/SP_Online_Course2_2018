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


def test_entry_conditions_valid():
    locke = Locke(5)
    locke.move_boats_through(5)

    assert locke.check_entry_conditions() is True


def test_entry_conditions_invalid():
    with pytest.raises(ValueError) as excinfo:
        locke = Locke(5)
        locke.move_boats_through(15)

    assert str(excinfo.value) == "{} accepts {} boats max."\
                                 .format(locke.size, locke.limit)


def test_doors(capsys):
    locke = Locke(5)

    locke.open_doors()

    captured = capsys.readouterr()
    assert captured.out == "Opening the doors.\n"

    locke.close_doors()

    captured = capsys.readouterr()
    assert captured.out == "Closing the doors.\n"


def test_move_boats_through(capsys):
    small_locke = Locke(5)

    small_locke.move_boats_through(5)

    captured = capsys.readouterr()
    assert captured.out == "Opening the doors.\n"\
                           "Closing the doors.\n"
