import pandas as pd
music = pd.read_csv("featuresdf.csv")

def favorite_generator(artist):
    for x in zip(music.artists,music.name):
        if x[0] == artist:
            yield x[1]

for x in favorite_generator('Kendrick Lamar'):
    print(x)