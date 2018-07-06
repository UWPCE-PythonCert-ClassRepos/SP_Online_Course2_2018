#!/usr/bin/env python3

#Natalie Rodriguez
#July 5, 2018
#Lesson 2

import pandas as pd
music = pd.read_csv("featuresdf.csv")

music_table = zip(music.name, music.artists)

music_titles = ((a, b)  for a, b  in music_table if b == 'Luis Fonsi')


print('               Song Title                |   Artist      ')
print('_________________________________________________________')
for m in music_titles:
    print(f'{m[0]:41}|{m[1]:21}\n')