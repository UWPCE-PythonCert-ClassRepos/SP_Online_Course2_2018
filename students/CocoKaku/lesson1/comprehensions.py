#!/usr/bin/env python3

"""
Lesson 1 Assignment: Comprehensions
"""


import pandas as pd
music = pd.read_csv("featuresdf.csv")
result = [x for x in zip(music.name,
                         music.artists,
                         music.danceability,
                         music.loudness)
          if x[2] > .8 and x[3] < -5]
result = sorted(result, key=lambda x: x[2], reverse=True)

headers = ("SONG TITLE", "ARTIST", "DANCEABILITY", "LOUDNESS")
print(f"{headers[0]:40} {headers[1]:20} {headers[2]:15} {headers[3]}")
for name, artists, danceability, loudness in result:
    print(f"{name:40} {artists:20} {round(danceability,3):<15} {round(loudness,3)}")
