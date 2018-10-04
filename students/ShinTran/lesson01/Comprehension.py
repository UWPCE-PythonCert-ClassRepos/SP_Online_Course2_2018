'''
Shin Tran
Python 220
Lesson 1 Assignment
'''

#!/usr/bin/env python3

# Get artists and song names for tracks with danceability
# scores over 0.8 and loudness scores below -5.0

import pandas as pd
music = pd.read_csv("featuresdf.csv")

filtered = zip(music.name, music.artists, music.danceability, music.loudness)

def get_dancability(table):
    return table[2]

comp = sorted([x for x in filtered if x[2] > 0.8 and x[3] < -5.0], key = get_dancability, reverse = True)[:5]

print("Song Name                                Artist          Danceability     Loudness")
print("----------------------------------------------------------------------------------")
for itr in comp:
    print('{:40} {:15} {:12,.5f} {:12,.5f}'.format(*itr))
