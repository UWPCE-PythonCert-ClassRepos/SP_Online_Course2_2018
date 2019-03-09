import pandas as pd
music = pd.read_csv("featuresdf.csv")
"""Write a closure to capture high energy tracks. High energy default is 0.8"""

def high_energy(min_energy1 = 0.8):
    min_energy = min_energy1
    def find_favorite():
        for artist, song, energy in zip(music.artists, music.name, music.energy):
            if energy >= min_energy:
                yield (artist, song, energy)
    return find_favorite()

if __name__ == '__main__':
    print('\n\nUsing a Generator to find your favorite Artist')
    favorites = high_energy()
    for x in favorites:
        print(x)
