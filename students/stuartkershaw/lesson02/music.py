#!/usr/bin/env python3

import pandas as pd
music = pd.read_csv("featuresdf.csv")

sorted_music = (f"{name}, {artists}" for name, artists in
                sorted(zip(music.name, music.artists))
                if artists == "Ed Sheeran")

for s in sorted_music:
    print(s)


def get_artist_tracks(artist_name):
    def get_energy_above(energy_level):
        return (f"{name}, {artists}: {energy}" for name, artists, energy in
                sorted(zip(music.name, music.artists, music.energy), reverse=True)
                if artists == artist_name and energy > energy_level)
    return get_energy_above


ed_tracks = get_artist_tracks("Ed Sheeran")
ed_high_energy = ed_tracks(0.8)

for s in ed_high_energy:
    print(s)
