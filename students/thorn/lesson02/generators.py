"""
Generators

Write a generator to find and print all of your favorite artist’s tracks from the data set - Post Malone in this case.
"""

import pandas as pd
music = pd.read_csv("featuresdf.csv")

# Get post songs
post_songs = [info for info in zip(music.artists, music.name) if info[0] == "Post Malone"]

# Print post songs
print("Post Malone Songs:")
for item in post_songs:
    print(item[1])