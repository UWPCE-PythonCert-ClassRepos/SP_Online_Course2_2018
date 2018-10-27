"""
Sean Tasaki
10/20/2018
Lesson02
generator
"""

#!/usr/bin/env python3

import pandas as pd

#returns tracks based on a multiplier for the track's energy level. 
def energy(mult):
    def get_energy_tracks():
        music = pd.read_csv("featuresdf.csv")
        return sorted([track for track in zip(music.artists, music.name, music.energy) if track[2] > mult],
        key =lambda x: x[2], reverse = True)
    return get_energy_tracks


if __name__ == "__main__":

    #Multiplier of 0.8
    energy_level = energy(0.8)
    for track in enumerate(energy_level(), 1):
        print(track)