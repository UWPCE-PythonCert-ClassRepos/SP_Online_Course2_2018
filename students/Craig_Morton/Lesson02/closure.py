# ------------------------------------------------- #
# Title: Lesson 2, Closure Assignment
# Dev:   Craig Morton
# Date:  11/20/2018
# Change Log: CraigM, 11/20/2018, Closure Assignment
# ------------------------------------------------- #

# !/usr/bin/env python3

import pandas as pd

tracks = pd.read_csv("featuresdf.csv")


def high_energy_tracks():
    songs = [z for z in zip(tracks.artists, tracks.name, tracks.energy) if z[2] >= .8]

    def music():
        for d in songs:
            print("Artist:", "\n", d[0], "Track:", d[1], "\n", "Energy:", d[2], "\n")
    return music


track_list = high_energy_tracks()
track_list()
