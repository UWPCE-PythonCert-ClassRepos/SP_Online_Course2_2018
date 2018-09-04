import pandas as pd

music = pd.read_csv("featuresdf.csv", encoding="cp1252")

data = list(zip(music.artists, music.name, music.loudness, music.danceability))

favorite_artist = "Ed Sheeran"

def fav(data, favorite_artist):
    for x in data:
        if x[0] == favorite_artist:
            yield x[1], x[0]

fav_artist_songs = fav(data, favorite_artist)

print("{:<35} | {:<14}".format("Track Name", "Artist"))
print("----------------------------------------------------------")
[print("{:<35} | {:<14}".format(str(x[0]), favorite_artist)) for x in fav_artist_songs]



