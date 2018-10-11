#!/usr/bin/env python3
import pandas as pd

__author__="Wieslaw Pucilowski"

music = pd.read_csv("featuresdf.csv")

def energy(level):
    selection = [x for x in zip(music.artists,
                                music.name,
                                music.energy)
                 if x[2] >= level]
    def energy_track():
        for i in selection:
            print("Artist: {}, Track: {}, Energy: {}"
                  .format(*i))
    return energy_track


if __name__ == "__main__":
    e = energy(0.8)
    e()
    