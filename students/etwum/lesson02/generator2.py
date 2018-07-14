
import pandas as pd

music = pd.read_csv("featuresdf.csv")

songs = [(a,b) for (a,b) in zip(music.artists, music.name) if a == "Kendrick Lamar"]

sorted_list = sorted(songs, key=lambda x: x[1], reverse=True)


def music_gen(tracks):
    # generator for finding favorite artist songs
    for x in tracks:
        yield x


favorite_artist_tracks = music_gen(sorted_list)

print(tuple(favorite_artist_tracks))