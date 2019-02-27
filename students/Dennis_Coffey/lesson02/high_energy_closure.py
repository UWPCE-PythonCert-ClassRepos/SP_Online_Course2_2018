# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 20:52:17 2019

@author: dennis
"""

"""Closure to capture high energy tracks. High energy tracks are anything over 0.8."""

import pandas as pd

# Import list of top hits from 2017
music = pd.read_csv("featuresdf.csv")

def get_high_energy_tracks(energy_level):
    
    def get_tracks():
        # Pull back only name, artists, danceability and loudness from top hits list
        music_list = list(zip(music.name, music.artists, music.danceability, music.loudness))
    
        # Filter list for songs with a certain energy level and sort so highest danceability songs are first
        return sorted([(name, artists, danceability, loudness) for name, artists, danceability, loudness in music_list if danceability > energy_level], key=lambda x: x[2], reverse=True)
        
    return get_tracks

high_energy_tracks = get_high_energy_tracks(0.8)
# Output top 5 hits for 2017 based on Danceability
print('Name' + ' '*38 + 'Artists' + ' '*10 + 'Danceability')
print('-'*75)
#print(high_energy_tracks)
for name, artists, danceability, loudness in high_energy_tracks():
    print('{:40}  {:15}  {:<20}'.format(name, artists, round(danceability,3)))
