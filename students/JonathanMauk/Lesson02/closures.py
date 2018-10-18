import pandas as pd


music = pd.read_csv("featuresdf.csv")


def high_energy_songs(energy=0.8):  # Default value is 0.8 but can be defined by user.
    def find_songs(song_list):
        return [song for song in zip(song_list.artists, song_list.name, song_list.energy) if song[2] > energy]
    return find_songs


