import pandas as pd
music = pd.read_csv("featuresdf.csv")

def high_energy():
    my_list = [songs for songs in zip(music.name, music.artists, music.energy) if songs[2] > 0.8]

    def print_high_energy():
        for songs in my_list:
            print(songs[0],' - ' , songs[1], songs[2])

    return print_high_energy()

high_energy()
