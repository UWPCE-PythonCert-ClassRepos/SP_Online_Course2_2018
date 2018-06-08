#!/usr/bin/env python3
"""Lesson2 Generators Module"""

import pandas as pd

music = pd.read_csv("featuresdf.csv")
tracks = (m for m in sorted(zip(music.artists, music.name),
                            key=lambda x: x[0], reverse=True)
          if m[0] == 'Ed Sheeran')

for track in tracks:
    print(f'{track[0]:<40}{track[1]:<40}')
