import pytest

from locke import Locke


def test_locke_init():
    with pytest.raises(Exception) as excinfo:
        locke = Locke()
    assert str(excinfo.value) == "__init__() missing 1 required positional "\
                                 "argument: 'limit'"

    locke = Locke(5)
    assert locke.limit == 5
