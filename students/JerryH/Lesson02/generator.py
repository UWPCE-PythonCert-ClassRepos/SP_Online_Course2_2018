#!/usr/bin/env python3

import pandas as pd
music = pd.read_csv("featuresdf.csv")

# Get all Ed Sheeran's tracks from the dataset
data = [m for m in
    sorted(zip(music.name, music.artists, music.danceability, music.loudness),
    key=lambda m: m[2], reverse=True) if m[1] == 'Ed Sheeran']

def track_generator(music_data):
    for i in music_data:
        yield i

ed_sheeran = track_generator(data)
print(next(ed_sheeran))
