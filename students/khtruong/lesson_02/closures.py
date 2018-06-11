#!/usr/bin/env python
import pandas as pd


def high_energy_tracks(energy=0.8):
    def find_tracks():
        gen = (metadata for metadata
               in zip(music.artists, music.name, music.energy)
               if metadata[2] > energy)
        for g in gen:
            print(f'{g[1]} -- {g[0]}, Energy = {g[2]}')
    return find_tracks

music = pd.read_csv("featuresdf.csv")
energy8 = high_energy_tracks()
energy8()
