#!/usr/bin/env python3

import pandas as pd
music = pd.read_csv("featuresdf.csv")

def getKey(item):
    return item[3]

def music_closure(energy = 0.8):

    music_table = zip(music.name, music.artists, music.danceability, music.energy)

    music_dance = sorted([(x, y, z, a) for x, y, z, a in music_table if a > energy],
                     key = getKey, reverse = True)


    def print_music():
        print(f'Title                                        |Artist              |Dance               |Energy Level = {energy} ')
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        for m in music_dance:
            print(f'{m[0]:45}|{m[1]:20}|{m[2]:20}| {m[3]:20} |\n')

    return print_music


if __name__ == "__main__":

    test_closure = music_closure()
    test_closure()
    print()
    print()
    test_closure9 = music_closure(0.9)
    test_closure9()