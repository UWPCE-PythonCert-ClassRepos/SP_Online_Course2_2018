'''
Shin Tran
Python 220
Lesson 2 Assignment
'''

#!/usr/bin/env python3

# Write a closure to capture high energy tracks
# we will define high energy tracks as anything over 0.8

import pandas as pd

music = pd.read_csv("featuresdf.csv")
music_list = zip(music.artists, music.name, music.energy)

def get_energy(table):
    return table[2]

def filter_list(energy):
    def high_energy():
        comp = [y for y in music_list if y[2] >= energy]
        return sorted(comp, key = get_energy, reverse = True)
    return high_energy

print("Artist               Song Name                                        Energy ")
print("-----------------------------------------------------------------------------")
track_list = filter_list(0.8)
for item in track_list():
    print('{:20} {:45} {:10,.5f}'.format(*item))