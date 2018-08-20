#!/usr/bin/env python3

#Natalie Rodriguez
#July 5, 2018
#Lesson 2

import pandas as pd
music = pd.read_csv("featuresdf.csv")

def getKey(item):
    return item[3]

def closure_music(energy = 0.8):

    music_table = zip(music.name, music.artists, music.danceability, music.energy)

    music_energy = sorted([(a, b, c, d) for a, b, c, d in music_table if d > energy],
                     key=getKey, reverse=True)


    def print_music():
        print(f'                    Song Title                      |          Artist           |        Danceability       |     Energy Level = {energy} ')
        print('___________________________________________________________________________________________________________________________________________')
        for m in music_energy:
            print(f'{m[0]:52}|{m[1]:27}|{m[2]:27}| {m[3]:27} |\n')

    return print_music


if __name__ == "__main__":
    test = closure_music()
    test()
    print()
    print()
    test4 = closure_music(0.4)
    test4()
    test5 = closure_music(0.5)
    test5()
