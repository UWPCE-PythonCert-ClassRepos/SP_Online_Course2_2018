# Brandon Henson
# Python 220
# Lesson 2
# 6-29-18

# !/usr/bin/env python3
import pandas as pd
from operator import itemgetter
music = pd.read_csv("featuresdf.csv")


def music_generator(a):
    for i in a:
        yield i


selection = (x for x in zip(music.name, music.artists, music.danceability,
             music.loudness) if x[1] == 'Ed Sheeran')

ed_sheeran = music_generator(selection)
print(next(ed_sheeran))
