#!/usr/bin/env python3
"""
Last week we looked at Spotify’s top tracks from 2017. 
We used comprehensions and perhaps a lambda to find tracks we might like. 
Having recovered from last week’s adventure in pop music we’re ready to venture back.

Write a generator to find and print all of your favorite artist’s 
tracks from the data set. Your favorite artist isn’t represented in that set? 
In that case, find Ed Sheeran’s tracks.

Load the data set following the instructions from last week. 
Submit your generator expression and the titles of your or Ed’s tracks.
"""
import pandas as pd

music = pd.read_csv("featuresdf.csv")

tracks = (x for x in zip(music.artists, music.name)
          if x[0] == 'Ed Sheeran')

for track in tracks:
    print(f'Artist: {track[0]} -- Track: {track[1]}')
