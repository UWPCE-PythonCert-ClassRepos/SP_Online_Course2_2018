'''
Lesson 1 Assignment #1
'''

import numpy as np
import pandas as pd #this code gives me an error message
music = pd.read_csv("featuresdf.csv")
#music.head()
#music.describe()

#[x for x in music.danceability if x > 0.8]

results = [(a,d,l) for a,d,l in zip(music.artists, music.danceability, music.loudness) if d > 0.8 and l < -0.5]

results2 = sorted(results, key=results.danceability) #this code is an issue, too.
results.head()

