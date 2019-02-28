"""Lesson 2 Closures Assignment
    Terrance J
    2/26/2019
"""

import pandas as pd 

def high_energy_tracks(energy):
    energy_min = energy
    music = pd.read_csv("featuresdf.csv")

    def get_high_energy_tracks():
        all_tracks = [(n,a,e) for n,a,e in zip(music.name,music.artists, music.energy)]  
        high_energy_list = []

        for track in all_tracks:
            if track[2] > energy_min:
                print(track[0],track[1],track[2])
        

    return get_high_energy_tracks()


if __name__ == '__main__':
    print(high_energy_tracks(0.8))
