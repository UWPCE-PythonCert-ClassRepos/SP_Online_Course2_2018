#!/usr/bin/env python3
# Ian Letourneau
# 8/27/2018

import gen_close as gc

sheeran_list = [
    "Shape of You",
    "Castle on the Hill",
    "Galway Girl",
    "Perfect",
]


def test_find_songs():
    """Function to test "find_songs" function. Asserts
    Ed Sheeran songs in expected list of outputs."""
    c = 0
    sheeran_gen = gc.find_songs("Ed Sheeran")
    for i in sheeran_gen:
        assert i in sheeran_list
        c += 1


def test_find_songs_close():
    """Function to test find_songs_close function. Asserts
    formatted output string of high energy songs."""
    ed = gc.find_songs_close("Ed Sheeran")
    high_energy_ed = ed(0.8)
    first = "{}, {}, {:0.3f}".format(
        high_energy_ed[0][0], high_energy_ed[0][1], high_energy_ed[0][2])
    assert first == "Ed Sheeran, Castle on the Hill, 0.834"


test_find_songs()
test_find_songs_close()
