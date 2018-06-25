"""
Generators

Write a generator to find and print all of your favorite artist’s tracks from the data set - Post Malone in this case.
"""

import pandas as pd
music = pd.read_csv("featuresdf.csv")

# Get post songs
def post_malone_songs(songs):
    for item in songs:
        yield item



if __name__ == "__main__":
    post_songs = (info for info in zip(music.artists, music.name) if info[0] == "Post Malone")

    songs = post_malone_songs(post_songs)

    for song in songs:
        print(song[1])



