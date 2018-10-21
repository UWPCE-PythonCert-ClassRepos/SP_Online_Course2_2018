#!/usr/bin/env python3

import pandas as pd

def find_tracks(artist_name, music):
    ''' Generator method to find tracks by artist '''
    for name, artist in zip(music.name, music.artists):
        if artist == artist_name:
            yield name

if __name__ == '__main__':
    music = pd.read_csv("featuresdf.csv")
    for track in find_tracks("Imagine Dragons", music):
        print(track)

# Result:
# Believer
# Thunder