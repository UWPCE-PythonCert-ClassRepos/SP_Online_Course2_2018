#!/usr/bin/env python3

import pandas as pd
music = pd.read_csv("featuresdf.csv")

data = [m for m in
    sorted(zip(music.name, music.artists, music.danceability, music.loudness),
    key=lambda m: m[2], reverse=True) if m[2] > 0.8 and m[3] < -0.5]

for m in data:
    print('{:40}\t{:20}\t{:5.3f}\t{:5.3f}'.format(m[0], m[1], m[2], m[3]))
