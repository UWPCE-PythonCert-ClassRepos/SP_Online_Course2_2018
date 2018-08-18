#!/usr/bin/env python3

import pandas as pd

def get_favorite_tracks():
    music = pd.read_csv("featuresdf.csv")
    for x in zip(music.artists, music.name):
        if x[0] == 'Ed Sheeran':
            yield x[1]

if __name__ == "__main__":
    for track in get_favorite_tracks():
        print(track)