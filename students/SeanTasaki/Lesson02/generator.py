"""
Sean Tasaki
10/20/2018
Lesson02
generator
"""

#!/usr/bin/env python3


import pandas as pd
music = pd.read_csv("featuresdf.csv")

def get_favorite_songs():
    for track in zip(music.artists, music.name):
        if track[0] == "Ed Sheeran":
            yield track

if __name__ == "__main__":
    for track in get_favorite_songs():
        print(track)