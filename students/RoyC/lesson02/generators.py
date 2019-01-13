#!/usr/bin/env python3
# Lesson 02, Generators

import pandas as pd

def get_artist_tracks(artist, music):
    ''' 
    Returns tracks by the given artist in the given music data set
    '''
    for track, artist_name in zip(music.name, music.artists):
        if artist == artist_name:
            yield track

if __name__ == '__main__':
    music = pd.read_csv("featuresdf.csv")
    print("Ed Sheeran's top tracks from 2017:\n")
    for track in get_artist_tracks("Ed Sheeran", music):
        print(track)

