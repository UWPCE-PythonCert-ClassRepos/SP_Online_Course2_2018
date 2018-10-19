#!/usr/bin/env python3

import pandas as pd

music = pd.read_csv("featuresdf.csv")


def main():
    string_format = "{:<20} | {:<20}"
    songs = drake_generator()

    print("{:<20} | {:<20}".format("Tracks", "Artist"))
    print("-"*35)
    for i in songs:
        print(string_format.format(*i))


# Generator that finds all of Drake's songs
def drake_generator():
    for x in zip(music.name, music.artists):
        if (x[1] == "Drake"):
            yield x


if __name__ == "__main__":
    main()
