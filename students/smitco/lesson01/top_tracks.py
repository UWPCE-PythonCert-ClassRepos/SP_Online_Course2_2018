# lesson 01 top tracks of 2017
# !/usr/bin/env python3

import pandas as pd
music = pd.read_csv("featuresdf.csv")

needed_info = list(zip(music.name, music.artists, music.danceability, music.loudness))
sorted_info = sorted(needed_info, key=lambda x: x[2], reverse= True)
print("Spotify Top Tracks 2017 by Danceability")
print("Danceability > 0.8, Loudness < -5.0")
print("")
count = 1
for i in sorted_info:
    if (i[2] > 0.8) and (i[3] < (-5.0)):
        print("{}) {} by {}\n   Danceability: {:.4f}   Loudness: {:.4f}".format(str(count), *i))
        count += 1