import pandas as pd
music = pd.read_csv("featuresdf.csv")


song_list = [ x for x in zip(music.name, music.artists, music.danceability, music.loudness) if x[2] > 0.8 and x[3] < -5]

def danceability_sort(x):
    return x[2]

for song in sorted(song_list, key=danceability_sort, reverse=True):
    print(song)