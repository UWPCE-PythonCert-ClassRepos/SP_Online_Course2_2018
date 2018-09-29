#!/usr/bin/env python3

import pandas as pd

music = pd.read_csv("featuresdf.csv")

tracks = sorted([x for x in zip(music.danceability, music.loudness, music.artists, music.name) if x[0] > 0.8 and x[1] < -5], reverse=True)

for track in tracks[:5]:
    print(track[2] + " - " + track[3])