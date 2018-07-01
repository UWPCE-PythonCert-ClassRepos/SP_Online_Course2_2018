# Brandon Henson
# Python 220
# Lesson 2
# 6-30-18

# !/usr/bin/env python3
import pandas as pd
from operator import itemgetter
music = pd.read_csv("featuresdf.csv")


def high_energy():
    selection = [x for x in zip(music.artists, music.name, music.energy) if x[2] >= .8]

    def print_music():
        for i in selection:
            print('Artist:', i[0], 'Track:', i[1], 'Energy:', i[2])

    return print_music

func = high_energy()
func()
