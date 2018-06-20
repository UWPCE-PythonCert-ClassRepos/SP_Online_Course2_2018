#!/usr/bin/env python3

import pandas as pd
music = pd.read_csv("featuresdf.csv")

ideal_songlist = [(artist, song) for danceable, volume, artist, song in sorted(
        zip(music.danceability, music.loudness, music.artists, music.name), 
        reverse=True) if danceable > 0.8 and volume < -5.0]

print("\n\t***Soft danceable song list!***\n")
print(f"RANK | {'ARTIST':<20} | {'SONG':<40}")
print(f"---- | {'-'*20} | {'-'*40}")
for i, j in zip(range(5), ideal_songlist[:5]):
    print(f'{i+1:>4} | {j[0]:<20} | {j[1]:<40}')
