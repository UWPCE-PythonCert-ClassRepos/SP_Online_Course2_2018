import pandas as pd
music = pd.read_csv("featuresdf.csv")

def favorite_generator(artist):
    for x in music.artists:
        if x == artist:
            yield x
            
for x in favorite_generator('Kendrick Lamar'):
    print(x)