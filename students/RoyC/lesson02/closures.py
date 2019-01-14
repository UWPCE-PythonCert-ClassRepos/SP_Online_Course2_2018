#!/usr/bin/env python3
# Lesson 02, Closures

import pandas as pd

def get_energetic_track_finder(energy):
    '''
    Return a getter tracks with energy equal to or higher than the given level
    '''
    def energetic_tracks(music):
        return [x for x in zip(music.name, music.artists, music.energy) if x[2] >= energy]
    return energetic_tracks

if __name__ == '__main__':
    music = pd.read_csv("featuresdf.csv")
    energy_over_80_pct = get_energetic_track_finder(0.8)
    print("{:<50}{:<20}{:>15}\n".format("Track", "Artist", "Energy"))
    for track in energy_over_80_pct(music):
        print("{:<50}{:<20}{:>15.4f}".format(track[0], track[1], track[2]))

