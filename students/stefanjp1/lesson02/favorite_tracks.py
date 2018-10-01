import pandas as pd
music = pd.read_csv("featuresdf.csv")


def get_favorite_tracks(music, fav_artist):
    for track in zip(music.name, music.artists):
        if track[1] == fav_artist:
            yield track

if __name__ == '__main__':
    print(*get_favorite_tracks(music, 'Ed Sheeran'))