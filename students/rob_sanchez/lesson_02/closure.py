#!/usr/bin/env python3

import pandas as pd

music = pd.read_csv("featuresdf.csv")


def main():
    string_format = "{:<20} | {:<20} | {:<20}"
    tracks = high_energy(0.8)

    print("{:<20} | {:<20} | {:<20}".format("Artist", "Track", "Energy"))
    print("-"*75)
    for i in tracks:
        print(string_format.format(*i))


# Closure that captures high energy tracks (anything over 0.8)
def high_energy(e=0.8):
    energy = e

    def tracks():
        track_list = [x for x in zip(music.artists, music.name,
                      round(music.energy, 3)) if (x[2] > energy)]
        return track_list
    return sorted(tracks(), key=lambda tup: tup[2], reverse=True)


if __name__ == "__main__":
    main()
