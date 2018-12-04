import pandas as pd
music = pd.read_csv("featuresdf.csv")

def favorite_generator(artist):
    for x in zip(music.artists,music.name):
        if x[0] == artist:
            yield x[1]

for x in favorite_generator('Kendrick Lamar'):
    print(x)

#use closure to capture high energy tracks (>0.8)

song_list = zip(music.artists,music.name,music.energy)

def high_energy(energy_level):
    def high(music):
        res = [(artist, song, energy) for (artist, song, energy) in song_list if energy > energy_level]
        print("k")
        return res
    return high

""" result = [(artist, song, energy) for (artist, song, energy) in song_list if energy > 0.8]
print(result) """

result = high_energy(0.8)
print(result)
