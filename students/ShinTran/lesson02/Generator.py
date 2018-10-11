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

def get_name(table):
    return table[1]

fav = sorted([x for x in music_list if x[0] == 'Martin Garrix'], key = get_name)

print("Artist               Song Name           ")
print("-----------------------------------------")
for itr in fav:
    print('{:20} {:20}'.format(*itr))