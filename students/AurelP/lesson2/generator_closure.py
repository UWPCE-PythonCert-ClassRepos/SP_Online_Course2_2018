#!/usr/bin/env python3
"""
    generator and closuer =lesson2
"""
import pandas as pd

def favorite(data, artist):
    """
        generator function
    """
    for x, y in data:
        if y == artist:
            yield (x, y)

def energy(a, b, c):
    """
        closure with generators
    """
    def high_energy(l):
        """
            generator function
        """
        for (x, y, z) in zip(a, b, c):
            if z >= l:
                #print (x,y,z)
                yield (str(x).encode('utf-8'), str(y).encode('utf-8'),
                       round(z, 2))
    return high_energy


if __name__ == "__main__":
    # I got an encoding when reading the file. i had to use utf-8 encoding
    music = pd.read_csv('featuresdf.csv', encoding='utf-8')
    artist = "Ed Sheeran"
    level = 0.8
    print("Favorite artist tracks: \n")
    #print(list(favorite(zip(music.name, music.artists), artist)))
    for i in favorite(zip(music.name, music.artists), artist):
        print(i)

    print(25*'---')
    print("Closure: high energy tracks:\n")
    he = energy(music.name, music.artists, music.energy)
    for i in he(level):
        print(i)
