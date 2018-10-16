#!/usr/bin/env python3

import pandas as pd

music = pd.read_csv("featuresdf.csv")


def main():
    comprehension_2()


# Comprehensions

# Songs with a Danceability score over 0.8
def comprehension_1():
    [print(x) for x in music.danceability if x > 0.8]


# Artists and song names for tracks with danceability scores over 0.8
# and loudness score below -5.0.
# Sort by danceability in descending order (most danceable tracks first)
def comprehension_2():
    string_format = ""
    songs = [x for x in zip(music.name, music.artists, music.danceability,
             music.loudness) if (x[2] > 0.8 and x[3] < -5.0)]

    songs = sorted(songs, key=lambda tup: tup[2], reverse=True)

    # Top 5 songs
    print("\nTop 5 most danceable songs: \n")
    [print("{:<40} | {:<20} | {:<20} | {:<10}".format(*x)) for x in songs[:5]]


# Generators
if __name__ == "__main__":
    main()
