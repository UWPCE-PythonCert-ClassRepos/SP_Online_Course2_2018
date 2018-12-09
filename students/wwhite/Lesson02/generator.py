#!/usr/bin/env python

"""
Write a generator to find and print all of your favorite artist’s tracks from the data set.
Your favorite artist isn’t represented in that set? In that case, find Ed Sheeran’s tracks.

Load the data set following the instructions from last week.
Submit your generator expression and the titles of your or Ed’s tracks.
"""

import pandas as pd
music = pd.read_csv("featuresdf.csv")

results = [songs[0] for songs in zip(music.name, music.artists) if songs[1] == "Ed Sheeran"]


def song_generator(music_list):
    for song in music_list:
        yield song


final_list = song_generator(results)


print(next(final_list))
