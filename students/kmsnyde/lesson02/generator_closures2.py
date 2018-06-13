# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 16:40:00 2018

@author: Karl M. Snyder
"""

import pandas as pd

# generator exercise

music = pd.read_csv('featuresdf.csv')

# genertor to produce Ed Sheeran tracks
fav_music = (("artist: ", artist, "track: ", song) for artist in music.artists for song in music.name if artist == "Ed Sheeran")

#print(next(fav_music))
#print(next(fav_music))
#print("\n\n")

# added per instructor feedback (vice using print statements)
for row in fav_music:
    print(row)

# closure exercise

def high_energy(level):
    def from_col(col):
        f = pd.read_csv('featuresdf.csv')
        res = [i for i in f[col] if i > level]
        return res
    return from_col

energy = high_energy(.8)
cols = sorted(energy('energy'), reverse=True)


high_e = [[artist, song, energy] for [artist, song, energy] in \
          zip(music.artists, music.name, music.energy) if energy in cols]

high_e_sort = sorted(high_e, key=lambda x: x[2], reverse=True)

# just to seperate outputs
print()
print()

for row in high_e_sort:
    print(row)