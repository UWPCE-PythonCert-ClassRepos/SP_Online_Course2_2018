#!/usr/bin/env python3
import pandas as pd

music = pd.read_csv("featuresdf.csv")

music.head()
music.describe()

def track_gen():
    for i in zip(music.name, music.artists):
        if i[1] == 'Ed Sheeran':
            yield i

track_list = [x for x in track_gen()]

print("Track List:")
print(track_list)

def energy_track_gen(energy):
    def energy_filter(music):
        my_list = [x for x in zip(music.artists, music.name, music.energy) if x[2]> energy]
        return my_list
    return energy_filter

energy_closure = energy_track_gen(0.8)
print(energy_closure(music))