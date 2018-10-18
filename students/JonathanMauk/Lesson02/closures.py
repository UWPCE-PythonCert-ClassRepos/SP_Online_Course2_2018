import pandas as pd


def songs_by_energy(energy=0.8):  # Default value is 0.8 to get high energy songs, but can be defined by user.
    def find_songs(song_list):
        return [song for song in zip(song_list.artists, song_list.name, song_list.energy) if song[2] > energy]
    return find_songs


music = pd.read_csv("featuresdf.csv")
high_energy_list = songs_by_energy()  # Using default value of 0.8.
high_energy_query = high_energy_list(music)  # Running data set through our closure.

for songs in high_energy_query:
    print(songs)
