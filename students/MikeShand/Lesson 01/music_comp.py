#!/usr/bin/env python3

import pandas as pd
music = pd.read_csv("featuresdf.csv")

def getKey(item):
    return item[2]

music_table = zip(music.name, music.artists, music.danceability, music.loudness)

music_dance = sorted([(x, y, z, a) for x, y, z, a in music_table if z > 0.8 and a < -0.5],
                     key = getKey, reverse = True)[0:5]

print('Title                              |Artist         |Dance   |Loudness')
print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
for m in music_dance:
    print(f'{m[0]:35}|{m[1]:15}|{m[2]:8}| {m[3]:10}\n')


