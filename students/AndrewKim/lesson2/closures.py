#!/usr/bin/env python3

import pandas as pd

def energy(energy_level):
    def get_energy_tracks():
        music = pd.read_csv("featuresdf.csv")
        return [track for track in zip(music.artists, music.name, music.energy) if track[2] > energy_level]
    return get_energy_tracks


if __name__ == "__main__":
    energy_over = energy(0.8)
    for track in energy_over():
        print("{}: {} has energy of {}".format(track[0], track[1], track[2]))