# ------------------------------------------------- #
# Title: Lesson 1, pt 1, Song Assignment
# Dev:   Craig Morton
# Date:  11/5/2018
# Change Log: CraigM, 11/5/2018, Song Assignment
# ------------------------------------------------- #

# !/usr/bin/env python3

import pandas as pd

music = pd.read_csv("featuresdf.csv")

songs_for_dancing = [x for x in zip(music.name, music.danceability, music.loudness) if x[1] > 0.8 and x[2] < -5]


def song_getter(dance):
    """Get songs with danceability scores above 0.8"""
    return dance[1]


song_list = sorted(songs_for_dancing, key=song_getter, reverse=True)

print("\nSongs list:\n")
for songs in songs_for_dancing[0:5]:
    print(songs[0])
