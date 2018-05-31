#!/usr/bin/env python
import pandas as pd

music = pd.read_csv("featuresdf.csv")
data = [metadata for metadata in
        zip(music.artists, music.name, music.danceability, music.loudness)
        if (metadata[2] > 0.8 and metadata[3] < -0.5)]
data = sorted(data, key=lambda x: x[2], reverse=True)
for d in data[:5]:
    print(f'{d[1]} - {d[0]}')
