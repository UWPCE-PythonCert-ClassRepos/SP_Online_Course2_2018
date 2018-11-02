import pandas as pd

MAX_ENERGY = 0.8
ARTIST_NDX = 0
NAME_NDX = 1
ENERGY_NDX = 2

# read in csv file for processing 
music = pd.read_csv("featuresdf.csv")

# closure that selects songs by energy level
def highEnergySongsClosure(energy):
    def selectSongs(music):
        songs = [x for x in zip(music.artists, music.name, music.energy) if x[ENERGY_NDX] > energy]
        return songs
    return selectSongs

songs = highEnergySongsClosure(MAX_ENERGY)

# print selected high energy songs 
print("{:20} {:55} {:16}".format("Artist","Name","Energy"))
print("-" *85)

for song in songs(music):
    print("{:20} {:45} {:15.1f}".format(song[ARTIST_NDX], song[NAME_NDX], song[ENERGY_NDX]))

