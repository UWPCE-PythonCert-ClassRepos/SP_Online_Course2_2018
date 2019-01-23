#!/usr/bin/env python3

import pandas as pd

music = pd.read_csv('featuresdf.csv')
top_5 = [(round(dance, 3), round(loud, 3), song_name, artist)
         for dance, loud, song_name, artist in zip(music.danceability, music.loudness, music.name, music.artists)
         if dance > 0.8 and loud < -5.0]

print('Top 5 Songs With Danceability > 0.8 and Loudness < -5.0:')
format_str = '{:<15}\t{:<10}\t{:<40}\t{:<20}'
print(format_str.format('Danceability', 'Loudness', 'Name', 'Artists'))
for i in sorted(top_5, key=lambda k: k[0], reverse=True)[:5]:
    print(format_str.format(*i))

