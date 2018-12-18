"""
test code for music_gen.py

"""

import pytest
import pandas as pd
from music_gen import songs_by


def test_songs_by():
    singer = 'Ed Sheeran'
    music = pd.read_csv("featuresdf.csv")
    song_gen = songs_by(music, singer)
    assert song_gen.__next__()[0] == 'Shape of You'
    assert song_gen.__next__()[0] == 'Castle on the Hill'
    assert song_gen.__next__()[0] == 'Galway Girl'
    assert song_gen.__next__()[0] == 'Perfect'
    with pytest.raises(StopIteration):
        song_gen.__next__()
