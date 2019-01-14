import pandas as pd
music = pd.read_csv("featuresdf.csv")

def my_favorite(artists_name):
    for name, artist in zip(music.name, music.artists):
        if artists_name == artist:
            yield name + ' | '

my_play_list = my_favorite("Ed Sheeran")
print(*my_play_list)
