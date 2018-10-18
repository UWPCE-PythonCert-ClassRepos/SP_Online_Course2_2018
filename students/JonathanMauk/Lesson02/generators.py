import pandas as pd


def songs_by_artist(a="Ed Sheeran"):  # Ed Sheeran is default but user can specify any artist string they want
    music = pd.read_csv("featuresdf.csv")
    for artist, song in zip(music.artists, music.name):
        if artist == a:
            yield song


for songs in songs_by_artist():
    print(songs)

# Should print following track titles by Ed Sheeran:
# Shape of You
# Castle on the Hill
# Galway Girl
# Perfect
