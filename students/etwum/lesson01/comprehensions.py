
import pandas as pd

music = pd.read_csv("featuresdf.csv")

songs = [(a,b,c,d) for (a,b,c,d) in zip(music.artists, music.name, music.danceability, music.loudness) if c > 0.8 and d > -5.0]

sorted_list = sorted(songs, key=lambda x: x[2], reverse=True)
print(sorted_list)


