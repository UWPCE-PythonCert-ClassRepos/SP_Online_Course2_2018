#!/usr/bin/env python3
"""List Comprehension Module"""

import pandas as pd


music = pd.read_csv("featuresdf.csv")

result = sorted([m for m in
                 zip(music.artists, music.name, music.danceability, music.loudness)
                 if m[2] > 0.8 and m[3] < -5.0],
                key=lambda m: m[2],
                reverse=True)[:5]

for m in result:
    print(f'{m[0]:20}\t{m[1]:40}\t{m[2]:5.3f}\t{m[3]:5.3f}')
