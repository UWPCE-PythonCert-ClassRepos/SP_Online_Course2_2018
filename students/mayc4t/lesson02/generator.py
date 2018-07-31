#!/usr/bin/env python3

import pandas as pd

# FileID: generator.py
#   Write a generator to find and print all of your favorite artist’s tracks
#   from the data set. Your favorite artist isn’t represented in that set? In
#   that case, find Ed Sheeran’s tracks.

music = pd.read_csv("featuresdf.csv")
ml = [x for x in zip(music.name, music.artists, music.danceability, music.loudness)]
ml.sort(key=lambda x: x[2], reverse=True)


def track_list(music_db):
    for i in music_db:
        if i[1] == "Ed Sheeran":
            yield i


print ("Ed Sheeran -- Music")
esm = track_list(ml)
for i in esm:
    print (i)
