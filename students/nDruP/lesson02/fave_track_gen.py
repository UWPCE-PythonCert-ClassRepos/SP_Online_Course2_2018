try:
    import sys
    import pandas as pd
except ModuleNotFoundError:
    print("Must use Python 2 for pandas module")
    sys.exit()

def fave_songs_by_artists(*fave_artist):
    music = pd.read_csv("featuresdf.csv")
    iter_tracks = iter([t for t, a in zip(music.name, music.artists)
                        if a in fave_artist])
    while True:
        yield next(iter_tracks)

if __name__ == "__main__":
    for a in fave_songs_by_artists('Ed Sheeran'):
        print(a)
    """
    for b in fave_songs_by_artists('Kendrick Lamar', 'Migos'):
        print(b)
    for c in fave_songs_by_artists('Childish Gambino', 'Lil Uzi Vert'):
        print(c)
    """
