#!/usr/bin/env python3

import pandas as pd

def get_favorite():
    music = pd.read_csv("featuresdf.csv")
    for s in zip(music.artists, music.name):
        if s[0] == 'Kendrick Lamar':
            yield s[1]

if __name__ == "__main__":
    for track in get_favorite():
        print(track)