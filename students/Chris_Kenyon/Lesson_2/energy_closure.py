#!/usr/bin/env python3

import pandas as pd

def above_energy(energy_level):
    def get_high_energy():
        music = pd.read_csv("featuresdf.csv")
        return [song for song in zip(music.artists, music.name, music.energy) if song[2] > energy_level]
    return get_high_energy


if __name__ == "__main__":
    energy = 0.8
    energy_lim = above_energy(energy)
    print("The following song have an energy level above {}!:".format(energy))
    for song in energy_lim():
        print("{} by {}({:.2f})".format(song[1], song[0], song[2]))