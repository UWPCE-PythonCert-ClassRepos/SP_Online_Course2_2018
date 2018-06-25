"""
Write a closure to capture high energy tracks (over 8.0).

Return artist name, track name and energy value.
"""

import pandas as pd
music = pd.read_csv("featuresdf.csv")

def get_tracks():
    # Find track, artist, energy if energy > 8.0
    tracks = [info for info in zip(music.artists, music.name, music.energy) if info[2] >= 0.8]

    def print_tracks():
        print("{:20}\t{:40}\t{:15}".format("Artist", "Track", "Energy Level"))
        for info in tracks:
            print(f"{info[0]:20}\t{info[1]:40}\t{info[2]:10.2f}")

    return print_tracks


run = get_tracks()
run()