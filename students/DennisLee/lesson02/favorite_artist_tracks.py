#!/usr/bin/env python3

import pandas as pd
music = pd.read_csv("featuresdf.csv")

def song_tracks(artist):
    for name, song in zip(music.artists, music.name):
        if name == artist:
            yield song


if __name__ == "__main__":
    a = song_tracks("Ed Sheeran")
    print(next(a))  # 'Shape of You'
    print(next(a))  # 'Castle on the Hill'
    print(next(a))  # 'Galway Girl'
    print(next(a))  # 'Perfect'
    print(next(a))  # StopIteration - only 4 songs from Ed Sheeran
