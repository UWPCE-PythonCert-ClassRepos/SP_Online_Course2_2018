# ------------------------------------------------- #
# Title: Lesson 2, Generator Assignment
# Dev:   Craig Morton
# Date:  11/19/2018
# Change Log: CraigM, 11/19/2018, Generator Assignment
# ------------------------------------------------- #

# !/usr/bin/env python3

import pandas as pd


def song_list(t="Ed Sheeran"):
    tracks = pd.read_csv("featuresdf.csv")
    for a, s in zip(tracks.artists, tracks.name):
        if a == t:
            yield s


if __name__ == '__main__':
    print("\nEd Sheeran songs: \n")
    for songs in song_list():
        print(songs)
