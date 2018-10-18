#!/usr/bin/env python3

"""
Closures
Using the same data set, write a closure to capture high energy tracks. 
We will define high energy tracks as anything over 0.8. 
Submit your code and the tracks it finds, artist name, track name and energy value.
"""

import pandas as pd

def high_energy_tracks(music, energy=0.8):
    music_energy = sorted([x for x in zip(music.artists, music.name, music.danceability,
                                          music.energy) if x[3] > energy], key=lambda x: x[3], reverse=True)
    def output():
        print(f'Tracks with energy level above: {energy:.2f}')
        for music in music_energy:
            print(f'{music[1]} by {music[0]}, Energy: {music[3]:.2f} with a danceability of {music[2]:.2f}')
        print()
    
    return output

music = pd.read_csv("featuresdf.csv")
energyof8 = high_energy_tracks(music)
energyof8()

#additional testing with different level

energyof5 = high_energy_tracks(music, .5)
energyof5()