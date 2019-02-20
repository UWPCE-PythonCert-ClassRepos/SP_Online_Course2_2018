# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 21:05:22 2019

@author: dennis
"""

"""Generator to produce list of tracks from my favorite artist - Ed Sheeran"""
import pandas as pd


# Generator to produce tracks from my favorite artist
def tracks(artist='Ed Sheeran'):
# Import list of top hits from 2017
    music = pd.read_csv("featuresdf.csv")
    
    # Pull back only name, artists, danceability and loudness from top hits list
    music_list = list(zip(music.name, music.artists, music.danceability, music.loudness))
    music_list = sorted([[name, artists, danceability, loudness] for name, artists, danceability, loudness in music_list if artists==artist], key=lambda x: x[0])
    i=0
    state = True
    while state == True:
        try:
            yield str(i+1) + ') ' + music_list[i][0]
            i += 1
        except:
            state = False
            continue
        
# Output favorite artist tracks
#g = tracks("Imagine Dragons")
g = tracks()
i = 0
print("My favorite artists tracks:")
while True:
    try:
        print(next(g))
        i += 1
    except:
        break