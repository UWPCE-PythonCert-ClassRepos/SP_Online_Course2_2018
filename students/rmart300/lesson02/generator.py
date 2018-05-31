"""
generator.py

1. Finds and prints my favorite artist’s tracks from the data set
2. Loads the data set following the instructions from last week. Submit your generator expression and the titles of your or Ed’s tracks.
"""

import pandas as pd

def get_drake_songs(song_artist_list):
    for x in song_artist_list:
       if x[1] == 'Drake':
           yield x[0]

music = pd.read_csv('featuresdf.csv')
names = [x for x in music.name]
artists = [x for x in music.artists]
all_songs = list(zip(names, artists))

drake_songs = get_drake_songs(all_songs)
print('Songs by Drake')
print('\n'.join(list(drake_songs)))
