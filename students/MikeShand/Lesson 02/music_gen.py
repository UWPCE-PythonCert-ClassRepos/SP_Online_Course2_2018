#!/usr/bin/env python3

import pandas as pd
music = pd.read_csv("featuresdf.csv")

music_table = zip(music.name, music.artists)

music_tracks = ((x, y)  for x, y  in music_table if y == 'Ed Sheeran')


print('Title                              |Artist         ')
print('+++++++++++++++++++++++++++++++++++++++++++++++++++')
for m in music_tracks:
    print(f'{m[0]:35}|{m[1]:15}\n')


