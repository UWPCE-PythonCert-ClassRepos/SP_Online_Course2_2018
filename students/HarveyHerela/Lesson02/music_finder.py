import pandas as pd

def get_favorite_song():
    music = pd.read_csv("featuresdf.csv")
    for data in zip(music.artists, music.name):
        if data[0] == 'The Chainsmokers':
            yield data[1]

if __name__ == "__main__":
    for song in get_favorite_song():
        print(song)

# Something Just Like This
# Paris
# Closer
# Don't Let Me Down