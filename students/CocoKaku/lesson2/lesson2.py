#!/usr/bin/env python3

"""
Assignment 2: Generators and Closures
"""

import pandas as pd
music = pd.read_csv("featuresdf.csv")

# Part 1: Generators
# Write a generator to find and print all of Ed Sheeran's tracks

def find_tracks(my_artist="Ed Sheeran"):
    """
    Generator that finds all tracks by a given artist
    :param my_artist: artist to find, defaults to Ed Sheeran
    :return: generator object containing song titles
    """
    for a_name, an_artist in zip(music.name, music.artists):
        if an_artist == my_artist:
            yield a_name

ed_songs = find_tracks()
bruno_songs = find_tracks("Bruno Mars")

print("Ed Sheeran Tracks")
while True:
    try:
        print("   " + next(ed_songs))
    except StopIteration:
        break

print("\nBruno Mars Tracks")
while True:
    try:
        print("   " + next(bruno_songs))
    except StopIteration:
        break

# Part 2: Closures
# Write a closure to capture high energy tracks

def make_energy_finder(min=0, max=1):
    """
    Closure that creates a generator for songs of a given energy level

    :param min: minimum energy, default is 0
    :param max: maximum energy, default is 1
    :return: generator function
    """
    def finder():
        nonlocal min
        nonlocal max
        for a_name, an_artist, an_energy in zip(music.name, music.artists, music.energy):
            if max >= an_energy >= min:
                yield a_name, an_artist, an_energy
    return finder

high_energy_song_gen = make_energy_finder(min=0.8)
high_songs = high_energy_song_gen()

print("\nHigh Energy Tracks")
while True:
    try:
        name, artist, energy = next(high_songs)
        print(f"   {name:45} {artist:20} {round(energy, 2):.2f}")
    except StopIteration:
        break
