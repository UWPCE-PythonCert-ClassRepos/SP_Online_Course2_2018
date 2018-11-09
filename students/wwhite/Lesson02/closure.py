#!/usr/bin/env python

"""
Using the same data set, write a closure to capture high energy tracks.
We will define high energy tracks as anything over 0.8.

Submit your code and the tracks it finds, artist name, track name and energy value.
"""

import pandas as pd
music = pd.read_csv("featuresdf.csv")


def high_energy_closure():
    results = [songs for songs in zip(music.name, music.artists, music.energy) if songs[2] > 0.8]

    def print_songs():
        for song in results:
            print(song[0], song[1], song[2])

    return print_songs

