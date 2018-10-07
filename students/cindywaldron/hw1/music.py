#!/usr/bin/env python3
import pandas as pd

music = pd.read_csv("featuresdf.csv")

music.head()
music.describe()


my_list = sorted([x for x in zip(music.danceability, music.loudness, music.artists, music.name) if x[0]> 0.8 and x[1] < -5.0 ], key = lambda x: x[0], reverse = True)


for i in range(len(my_list)):
    if i > 4:
        break
    print(my_list[i])