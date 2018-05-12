#!/usr/bin/env python3

import pandas as pd
music = pd.read_csv("featuresdf.csv")

def make_high_energy_tracks():
    data = [m for m in
        sorted(zip(music.name, music.artists, music.energy),
        key=lambda m: m[2], reverse=True) if m[2] >= 0.8]

    def print_tracks():
        for m in data:
            print('{:40}\t{:20}\t{:5.3f}'.format(m[0], m[1], m[2]))

    return print_tracks

my_func = make_high_energy_tracks()
my_func()
