#!/usr/bin/env python3

import pandas as pd

music = pd.read_csv("featuresdf.csv")


def find_artist(songs, artist):
    for song in songs:
        if song[0] == artist:
            yield song


ed = find_artist([x for x in zip(music.artists, music.name)], "Ed Sheeran")

while True:
    try:
        song = next(ed)
        print("{} - {}".format(song[0], song[1]))
    except StopIteration:
        break
