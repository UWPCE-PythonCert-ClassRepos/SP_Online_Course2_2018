"""
test code for music_closure.py

"""

import pytest
import pandas as pd
from music_closure import make_upper_att_filter


def test_make_upper_att_filter():
    attribute = 'energy'
    min_value = 0.8
    music = pd.read_csv("featuresdf.csv")
    energy_filter = make_upper_att_filter(attribute, min_value)
    loudness_filter = make_upper_att_filter('loudness', -3.)
    high_energy = energy_filter(music)
    loud = loudness_filter(music)
    assert high_energy[0][2] == 0.815
    assert high_energy[1][2] == 0.812
    assert loud[0][0] == 'Chantaje'
    assert loud[1][0] == 'Solo Dance'