# Comprehensions
import pandas as pd
music = pd.read_csv('featuresdf.csv')

music_zip = zip(music.danceability, music.name, music.artists, music.loudness)
music_list = sorted([x for x in music_zip if x[0] > 0.8 and x[3] < -5.0], reverse = True)
[print(x[2], '-', x[1]) for x in music_list[:5]]