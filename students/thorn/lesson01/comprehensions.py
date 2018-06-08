"""
Pop music research with Pandas
"""

import pandas as pd


music = pd.read_csv("featuresdf.csv")

# print(music.head())         
# print(music.describe())

# Goal: Get artists and song names for tracks with danceability scores > 0.8 and loudness < -5.0
#       Sorted in descending order by danceability (most danceable up top)

goal = sorted([info for info in zip(music.artists, music.name, music.danceability, music.loudness) 
            if info[2] > 0.8 and info[3] < -5.0], key=lambda info: info[2], reverse=True)

goal = goal[:5]

print(goal)



