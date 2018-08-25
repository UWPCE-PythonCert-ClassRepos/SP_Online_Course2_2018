import pandas as pd
from memory_profiler import profile

music = pd.read_csv("featuresdf.csv")

songs = [(a,b,c) for (a,b,c) in zip(music.artists, music.name, music.energy) if c > 0.8]

sorted_list = sorted(songs, key=lambda x: x[1], reverse=True)


@profile()
def energy_tracks(tracks):
    def music_gen():
        for x in tracks:
            print(x)
    return music_gen


energy = energy_tracks(sorted_list)

energy()


