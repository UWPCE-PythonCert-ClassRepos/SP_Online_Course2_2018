#-------------------------------------------------#
# Title: Closures
# Dev:   LDenney
# Date:  February 6th, 2019
# ChangeLog: (Who, When, What)
#   Laura Denney, 2/6/19, Started work on closures assignment
#-------------------------------------------------#

import pandas as pd
music = pd.read_csv("featuresdf.csv")

def high_energy(constant_energy):
    def energy_fun(song_energy):
        return song_energy > constant_energy
    return energy_fun

high = high_energy(0.8)
name_artist_energy = list(zip(music.name, music.artists, music.energy))


lst_energysongs = [(name, artists, energy) for name, artists, energy in name_artist_energy if high(energy) ]

str_energy = '''
             High Energy Songs 2017         | Energy | Artist
--------------------------------------------------------------'''
strformat = '\n{:<45}{:<9.3}{:<13}'
for name,artist, energy in lst_energysongs:
    str_energy +=  strformat.format(name,energy, artist)

print(str_energy)