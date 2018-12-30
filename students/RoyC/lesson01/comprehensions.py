#!/usr/bin/env python3
# Lesson 01, Comprehensions

import pandas as pd
music = pd.read_csv("featuresdf.csv")

toptracks = sorted([x for x in zip(music.danceability, music.loudness, music.artists, music.name) if x[0] > 0.8 and x[1] < -5], reverse=True)

for track in toptracks[:5]:
    print(track[3] + " by " + track[2])