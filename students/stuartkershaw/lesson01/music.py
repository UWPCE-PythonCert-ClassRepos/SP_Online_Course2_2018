#!/usr/bin/env python3

import pandas as pd
music = pd.read_csv("featuresdf.csv")

sorted_music = [f"{name}, {title}" for x, y, name, title in
                sorted(zip(music.danceability,
                           music.loudness,
                           music.name,
                           music.artists), reverse=True)
                if x > 0.8 and y < -0.5]

print('\n'.join(sorted_music))
