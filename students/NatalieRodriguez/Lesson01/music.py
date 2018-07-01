#!/usr/bin/env python 3

#Natalie Rodriguez
#UW Python - Course 2
#Lesson 1: Comprehensions
#June 28, 2018

import pandas as pd
music = pd.read_csv("featuresdf.csv")

def musicInfo(item):
    return item[2]

music_table = zip(music.name, music.artists, music.danceability, music.loudness)

music_specs = sorted([(a, b, c, d) for a, b, c, d in music_table if c > 0.8 and d < -0.5]),
                     key = musicInfo, reverse = True)[0:5]

print('Title                                             |Artist              |Danceability   |Loudness    ')
print('____________________________________________________________________________________________________________')
for m in music_specs:
    print(f'{m[0]:50}|{m[1]:20}|{m[2]:15}| {m[3]:12}\n')