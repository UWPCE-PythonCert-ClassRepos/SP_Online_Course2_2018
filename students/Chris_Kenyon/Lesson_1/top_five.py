#!/usr/bin/env python
# Lesson 1: Top 5 music sorting/selecting, learning comprehensions

import pandas as pd
music = pd.read_csv("featuresdf.csv")


def top_five():
    sorted_music = sorted(
        [(artist, name, dance, loud) for artist, name, dance, loud in zip(
            music.artists, music.name, music.danceability, music.loudness
            ) if dance > 0.8 if loud < 0.5]
        )
    top_five = sorted_music[0:5]
    return top_five
