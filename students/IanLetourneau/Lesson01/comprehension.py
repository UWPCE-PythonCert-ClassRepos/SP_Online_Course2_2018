#!/usr/bin/env python3
# Ian Letourneau
# 8/27/2018

import pandas as pd 
music = pd.read_csv("featuresdf.csv")

small_music = music.loc[:, ['name', 'artists', 'danceability', 'loudness']]
top_dance = [(a,d) for a,d in zip(music.artists,music.danceability) if d > 0.8]
top_tracks = [(a,n,d,l) for a,n,d,l in zip(music.artists,music.name,music.danceability,music.loudness) if d > 0.8 and l < -0.5]
top_tracks = sorted(top_tracks, key=lambda track: track[2], reverse=True)


for item in range(5):
    print ("{}, {}".format(top_tracks[item][0], top_tracks[item][1]))
