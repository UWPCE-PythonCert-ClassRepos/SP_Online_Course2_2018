import pandas as pd

music = pd.read_csv("featuresdf.csv")

song_list = [x for x in zip(music.danceability, music.loudness, music.name, music.artists)
             if x[0] > 0.8 and x[1] < -5]

for x in song_list:
    print(x)
