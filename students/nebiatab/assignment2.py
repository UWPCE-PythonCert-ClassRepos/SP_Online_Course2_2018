# Nebiat
# hw2 Generators and Closures

import pandas as pd
music = pd.read_csv("featuresdf.csv")


# Lists favorite artists using generator
def fav_artists_wGen(name):
    # rows that favorite artist appears
    rows = music.index[music.artists == name]
    # returns name of song in that row
    song_name = (music.at[x, "name"] for x in rows)
    return song_name

# Using closure to find high energy songs
def high_energy(name, artists, danceability):
    def energy_songs(level):
        music = pd.read_csv("featuresdf.csv")
        music = music[[name, artists, danceability]]
        return music[music.danceability > level]
    return energy_songs
    

# Loops through generator
for each_song in fav_artists_wGen("Ed Sheeran"):
    print(each_song)

# Finds songs with danceability higher than .8 using closure
energy = high_energy("name", "artists", "danceability")
energy(.8)

