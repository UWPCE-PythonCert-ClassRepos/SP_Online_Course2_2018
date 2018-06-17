#!/usr/bin/env python3

import pandas as pd

music = pd.read_csv("featuresdf.csv")

songs = [x for x in zip(music.artists, music.name, music.energy)]


def make_tester(threshold):
    def check_song(song):
        if song[2] > threshold:
            print("{} - {}".format(song[0], song[1]))
    return check_song


energy_point8 = make_tester(0.8)

for song in songs:
    energy_point8(song)
