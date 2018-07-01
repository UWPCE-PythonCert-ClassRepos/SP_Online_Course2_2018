#!/usr/bin/env python3

from itertools import count
import pandas as pd
music = pd.read_csv("featuresdf.csv")

def high_energy_song_generator(threshold):
    def func():
        for artist, track, spunk in zip(
                music.artists, music.name, music.energy):
            if spunk >= threshold:
                yield (artist, track, spunk)
    return func


if __name__ == "__main__":
    e_80_function = high_energy_song_generator(0.8)
    val = e_80_function()
    print("\n\t***HIGH ENERGY SONGS***\n")
    print("{0:>5} | {1:<18} | {2:<44} | {3:<12}".format(
            "COUNT", "ARTIST", "SONG", "ENERGY LEVEL"))
    print("-"*5, "|", "-"*18, "|", "-"*44, "|", "-"*12)
    counter = count(1)
    while True:
        i = next(counter)
        try:
            e_80_song = next(val)
        except StopIteration:
            print("\n\t***THE END***")
            break
        else:
            print("{0:>5} | {1:<18} | {2:<44} | {3:>12.3f}".format(i, *e_80_song))
