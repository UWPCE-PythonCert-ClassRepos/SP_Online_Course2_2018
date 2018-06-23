# Brandon Henson
# Python 220
# Lesson 1
# 6-20-18

# !/usr/bin/env python3
import pandas as pd
from operator import itemgetter
music = pd.read_csv("featuresdf.csv")

selection = [x for x in zip(music.name, music.artists, music.danceability, \
             music.loudness) if x[2] > 0.8 and x[3] < -5]

final_list = sorted(selection, key=itemgetter(2), reverse=True)[:5]

for i in final_list:
    print(i[0], " ----- ", i[1])
