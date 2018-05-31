"""

closure.py

1. A closure to capture high energy tracks (>8.0)
2. Submit your code and the tracks it finds, artist name, track name and energy value.

"""

import pandas as pd

def filter_songs_by_energy(energy):  # line 1
     def filter_songs(song_list):  # line 2
         return [x for x in song_list if x[2] > energy]
     return filter_songs

music = pd.read_csv('featuresdf.csv')
names = [x for x in music.name]
artists = [x for x in music.artists]
energy = [x for x in music.energy]
all_songs = list(zip(names, artists, energy))

energy_filter = filter_songs_by_energy(0.8) 
energy8_songs = energy_filter(all_songs)
print('Songs with energy > 0.8')
print('\n'.join([f"{x[0]} by {x[1]} has energy {round(x[2],2)}" for x in energy8_songs]))

