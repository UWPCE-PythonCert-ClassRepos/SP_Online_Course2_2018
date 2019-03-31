"""Lesson 2 Generators Assignment
   Terrance J
   2/26/2019
"""

import pandas as pd 

def fav_tracks(artist):
    """Generator that yields all of your favorite artists songs on the top 100 list"""
    
    music = pd.read_csv("featuresdf.csv")

    top_tracks = [(n,a) for n,a in zip(music.name,music.artists)]  

    for track in top_tracks:
        if track[1] == artist:
            yield track[0],track[1]


if __name__ == '__main__':
    
    my_tracks = fav_tracks("Ed Sheeran")
    
    for i in my_tracks:
        print(i)