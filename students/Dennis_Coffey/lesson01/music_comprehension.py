# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 20:35:37 2019

@author: dennis
"""
"""Job to get artists and song names for for tracks with danceability scores over 0.8 and loudness scores below -5.0."""

import pandas as pd

# Import list of top hits from 2017
music = pd.read_csv("featuresdf.csv")

# Pull back only name, artists, danceability and loudness from top hits list
music_list = list(zip(music.name, music.artists, music.danceability, music.loudness))
# Filter list for songs with high danceability and low loudness and sort so highest danceability songs are first
music_list = sorted([(name, artists, danceability, loudness) for name, artists, danceability, loudness in music_list if danceability > 0.8 and loudness < -5.0], key=lambda x: x[2], reverse=True)

# Output top 5 hits for 2017 based on Danceability
print('Name' + ' '*38 + 'Artists' + ' '*10 + 'Danceability' + ' '*10 + 'Loudness')
print('-'*95)
for name, artists, danceability, loudness in music_list[:5]:
    print('{:40}  {:15}  {:<20}  {:<10}'.format(name, artists, round(danceability,3), loudness))