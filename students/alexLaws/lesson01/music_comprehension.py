#!/usr/bin/env python3

import pandas as pd

music = pd.read_csv("featuresdf.csv")

quiet_dance_songs = [x for x in zip(music.name, music.artists,
                     music.danceability, music.loudness) if x[2] > 0.8 and x[3] < -5]

top_5 = sorted(quiet_dance_songs, key=lambda x: x[2], reverse=True)[:5]

print("The Best Songs Are:")
for song in top_5:
    print("{} - {}".format(song[0], song[1]))
