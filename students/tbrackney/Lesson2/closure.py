"""
File Name: closure.py
Author: Travis Brackney
Class: Python 220 - Self paced online
Date Created 1/27/2019
Python Version: 3.6.4
"""
import pandas as pd


def energy_closure(dataset):
    def find_tracks(energy, data=dataset):
        tracks = zip(data.name, data.artists, data.energy)
        return [(song, artist, eng) for song, artist, eng in tracks if eng > energy]
    return find_tracks


music = pd.read_csv("featuresdf.csv")
get_energy = energy_closure(music)
tracks = get_energy(0.8)
for track in tracks:
    print(track)
