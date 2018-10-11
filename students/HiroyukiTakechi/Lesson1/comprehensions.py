'''
Lesson 1 Assignment #1
'''

import numpy as np
import pandas as pd #this code gives me an error message
music = pd.read_csv("featuresdf.csv")
#music.head()
#music.describe()

#[x for x in music.danceability if x > 0.8]

def get_danceability(result):
    return -result[1]

results = sorted([(a,d,l) for a,d,l in zip(music.artists, music.danceability, music.loudness) if d > 0.8 and l < -0.5], key=get_danceability)


for i, result in enumerate(results):
    if i < 5:
        print(result)

