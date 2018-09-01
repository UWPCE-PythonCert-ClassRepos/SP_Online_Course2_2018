import pandas as pd


def findsong(data, energy_level):

    songs = [x for x in data if x[2] > energy_level]

    def songprinter():
        [print("{:<42} | {:<17} | {:<10}".format(str(song[1]), song[0], song[2])) for song in songs]

    return songprinter()


music = pd.read_csv("featuresdf.csv", encoding="cp1252")

data = list(zip(music.artists, music.name, music.energy))

print("{:<42} | {:<17} | {:<10}".format("Track Name", "Artist", "Energy Level"))
print("-----------------------------------------------------------------------")

songFinder = findsong(data, 0.8)
songFinder
