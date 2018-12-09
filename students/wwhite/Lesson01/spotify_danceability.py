#!/usr/bin/env python

"""
Get artists and song names for for tracks with danceability scores over 0.8 and loudness scores below -5.0.
In other words, quiet yet danceable tracks.
Also, these tracks should be sorted in descending order by danceability so that the most danceable tracks are up top.
"""

import pandas as pd
music = pd.read_csv("featuresdf.csv")

#  Songs with danceability scores over 0.8
danceable = [x for x in music.danceability if x > 0.8]

#  Get the artist and song name from 'music' where danceability > 0.8 and loudness < -5.0
results = sorted([(a, b, c, d) for a, b, c, d in zip(music.name, music.artists, music.danceability, music.loudness) if
                 c > 0.8 and d < -5], key=lambda tup: tup[2], reverse=True)

final_results = [(a[0], a[1]) for a in results]

print(final_results)
