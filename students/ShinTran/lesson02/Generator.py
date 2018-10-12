'''
Shin Tran
Python 220
Lesson 2 Assignment
'''

#!/usr/bin/env python3

# Write a generator to find and print all of your favorite artist’s tracks
# from the data set; Martin Garrix

import pandas as pd
music = pd.read_csv("featuresdf.csv")

music_list = zip(music.artists, music.name)

fav = (x for x in music_list if x[0] == 'Martin Garrix')

print("  Artist           Song Name             ")
print("-----------------------------------------")
print(next(fav))
print(next(fav))
print(next(fav))