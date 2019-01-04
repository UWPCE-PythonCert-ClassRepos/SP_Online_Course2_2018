#!/usr/bin/env python3

import pandas as pd

music = pd.read_csv("featuresdf.csv")


list3 = [x for x in zip(music.artists, music.name) if x[0] == "Ed Sheeran"]

print("List of all the songs by a favorite artist:")
for x in list3:
    print ('{:30} {:50}'.format(x[0], x[1]))
