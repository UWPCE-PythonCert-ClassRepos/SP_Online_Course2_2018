#-------------------------------------------------#
# Title: Context Managers: Lockes TEST
# Dev:   LDenney
# Date:  February 11th, 2019
# ChangeLog: (Who, When, What)
#   Laura Denney, 2/13/19, Started work on context Managers Assignment
#-------------------------------------------------#

from context_manager_locke import Locke

def locke_test(locke, boats):
    with locke as spectacle:
            spectacle.move_boats_through(boats)

def test_arg():
    locke = Locke(3)
    assert repr(locke)=="Locke capacity is 3 boats."

def test_toomanyboats1():
    small_locke = Locke(4)
    boats = 5
    try:
        locke_test(small_locke, boats)
    except Exception as e:
        assert type(e) is ValueError

def test_rightamountboats1():
    small_locke = Locke(4)
    boats = 4
    try:
        locke_test(small_locke, boats)
    except Exception as e:
        assert type(e) is ValueError
    finally:
        print("passed")

def test_toomanyboats2():
    large_locke = Locke(8)
    boats = 28
    try:
        locke_test(large_locke, boats)
    except Exception as e:
        assert type(e) is ValueError

def test_rightamountboats2():
    large_locke = Locke(8)
    boats = 4
    try:
        locke_test(large_locke, boats)
    except Exception as e:
        assert type(e) is ValueError
    finally:
        print("passed")
