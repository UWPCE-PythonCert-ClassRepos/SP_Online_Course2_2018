#!/usr/bin/env python3


import pandas as pd

music = pd.read_csv('featuresdf.csv')

top_5 = []
for dance, loud, song_name, artist in zip(music.danceability, music.loudness, music.name, music.artists):
    if dance > 0.8 and loud < -5.0:
       top_5.append([dance, loud, song_name, artist])

all_values_sorted = sorted(top_5, key=lambda k: k[0], reverse=True)

print('Top 5 Songs With Danceability > 0.8 and Loudness < -5.0:')
format_str = '{:<20}\t{:<20}\t{:<30}\t{:<20}'
print(format_str.format('Danceability', 'Loudness', 'Name', 'Artists'))
for i in all_values_sorted[:5]:
    print(format_str.format(*i))

