#!/usr/bin/env python3
# Lesson1 comprehension - Aurel Perianu

import pandas as pd
music = pd.read_csv('featuresdf.csv')

data = sorted(zip(music.name, music.artists, music.danceability,
                  music.loudness), key=lambda x: x[2], reverse=True)

data = [(a, b, c, d) for a, b, c, d in data if c > 0.8 and d < -5]

[print(x) for x in data]
