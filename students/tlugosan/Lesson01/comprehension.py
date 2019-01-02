#!/usr/bin/env python3

import pandas as pd

music = pd.read_csv("featuresdf.csv")

[x for x in music.danceability if x > 0.8]

list1 = sorted([x for x in zip(music.artists, music.name, music.danceability, music.loudness) if x[2] > 0.8 and x[3] < -5.0], key = lambda x : x[2], reverse=True)

for x in list1:
    print ('{:30} {:40} {:.4f} {:.4f}'.format(x[0], x[1], x[2], x[3]))

print ("-------------------------------------------")

list2 = sorted([x for x in zip(music.artists, music.name, music.danceability, music.loudness) if x[2] > 0.8 and x[3] < -5.0], key = lambda x : x[2], reverse=True)[:5]

for x in list2:
    print ('{:30} {:40} {:.4f} {:.4f}'.format(x[0], x[1], x[2], x[3]))
