#!/usr/bin/env python3
import pandas as pd

__author__="Wieslaw Pucilowski"

music = pd.read_csv("featuresdf.csv")

def Find_Artist(artist="Ed Sheeran"):
    selection  = [x for x in list(zip(music.name,
                                      music.artists))
                  if x[1] == artist]
    def music_gen():
        for i in selection:
            yield i
    return music_gen


if __name__ == "__main__":
    g = Find_Artist(artist="Ed Sheeran")()
    while True:
        try:
            print("{}, {}".format(*next(g)))
        except StopIteration:
            print("+++ This is the end +++")
            break