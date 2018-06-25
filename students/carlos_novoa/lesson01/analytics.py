#!/usr/bin/env python3

import pandas as pd

"""
Lesson1 - Comprehensions
"""

music = pd.read_csv("featuresdf.csv")

# m_head = music.head
# m_description = music.describe

top_tracks = [f'{i+1}) {c} by {d}' for i, (a, b, c, d) in
              enumerate(sorted(zip(music.danceability,
                                   music.loudness,
                                   music.name,
                                   music.artists), reverse=True))
              if a > 0.8 and b < -5.0][:5]

print(*top_tracks, sep='\n')
