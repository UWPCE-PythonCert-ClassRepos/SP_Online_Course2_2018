# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 13:31:05 2018

@author: Karl M. Snyder
"""

import pandas as pd

music = pd.read_csv('featuresdf.csv')

best_tracks = [[a, b, c, d] for [a, b, c, d] in zip(music.artists, music.name, 
                music.danceability, music.loudness) if c > .8 and 
                d < -5]

best_tracks_sorted = sorted(best_tracks, key=lambda x: x[2], reverse=True)
my_tracks = [x[1] for x in best_tracks_sorted]
# Top five tracks
print(my_tracks[:5])
