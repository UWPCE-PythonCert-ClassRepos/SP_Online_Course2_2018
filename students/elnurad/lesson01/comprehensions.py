#!/usr/bin/env python
import pandas as pd

music = pd.read_csv("featuresdf.csv")

music.head()
music.describe()

songs = (sorted([song for song in zip(music.artists, music.name, music.danceability, music.loudness) if song[2] > 0.8 and song[3] < -0.5],key = lambda song: song[2], reverse = True))

top_five = songs[:5]

def top_five_songs():
    print("The top five songs in the list")
    print("{:<20}{}".format("Artist", "Name"))
    print("----------------------------------------")
    for a_song in top_five:
        print("{:<20}{}".format(a_song[0],a_song[1]))


if __name__ == "__main__":
    top_five_songs()


