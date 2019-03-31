#!/usr/bin/env python
import pandas as pd

music = pd.read_csv("featuresdf.csv")
fav_artist = zip(music.artists, music.name)

# generator function
def fav_artist_in_file():
    for value in fav_artist:
        if value[0] == "Ed Sheeran":
            yield value


#generator comprehension
artist_generator = (value for value in fav_artist if value[0] == "Ed Sheeran")


def printing():
    while True:
        try:
            print(next(artist_generator))
        except StopIteration:
            break


if __name__ == "__main__":
    print("Ed Sheeran's songs are:")
    printing()






  









