#!/usr/bin/env python3
# Ian Letourneau
# 8/27/2018

import pandas as pd
music = pd.read_csv("featuresdf.csv")


def find_songs(artist="Ed Sheeran"):
    """A function to generate songs based on given artist name 
    (default Ed Sheeran)"""
    songs = [(a, n) for a, n in zip(music.artists, music.name) if a == artist]
    for track in songs:
        yield track[1]


def find_songs_close(artist="Ed Sheeran"):
    """A function to store the high energy closure function based on given artist.
    The closure function will be callable with a given energy level(default 0.8)
    to return a tuple of artist, song name,and energy value."""
    songs = [(a, n) for a, n in zip(music.artists, music.name) if a == artist]

    def energy_songs(energy=0.8):
        songs = [(a, n, e) for a,
                 n, e in zip(music.artists,
                             music.name, music.energy)if e > energy and a == artist]
        return songs
    return energy_songs
