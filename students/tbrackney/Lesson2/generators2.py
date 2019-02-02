"""
File Name: generators2.py
Author: Travis Brackney
Class: Python 220 - Self paced online
Date Created 1/27/2019
Python Version: 3.6.4
"""

import pandas as pd

music = pd.read_csv("featuresdf.csv")


def track_lister(artist_name, ds=music):
    # return (song for (song, art) in zip(ds.name, ds.artists) if art == artist)
    for song, artist in zip(ds.name, ds.artists):
        if artist == artist_name:
            yield song


print("Tracks by Kendrick Lamar")
tl = track_lister('Kendrick Lamar')
for x in tl:
    print(x)

# Songs:
# HUMBLE.
# DNA.
