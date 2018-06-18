#!/usr/bin/env python
""" A closure that captures list of high energy tracks """

import pandas as pd
music = pd.read_csv("featuresdf.csv")

# Return track name, artist, and energy value

def make_track_finder():
    def find_tracks(e):
        return [(name, artist, energy) for (name, artist, energy) in zip(music.name, music.artists, music.energy) if energy > e]
    return find_tracks