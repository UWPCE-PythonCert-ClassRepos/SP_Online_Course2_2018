#!/usr/bin/env python3

import pandas as pd

music = pd.read_csv("featuresdf.csv")


def high_energy_songs(energy=0.8):
    def favorite_artist(artist="Ed Sheeran"):
        return[x for x in zip(music.artists, music.name, music.energy) if x[0] == artist and x[2] >= energy]
    return favorite_artist
