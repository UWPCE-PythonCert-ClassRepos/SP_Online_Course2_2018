try:
    import sys
    import pandas as pd
except ModuleNotFoundError:
    print("Must use Python 2 for pandas module")
    sys.exit()

music = pd.read_csv("featuresdf.csv")

song_artist = [(n, a) for n, a in zip(music.name, music.artists)]
song_artist_str = ("{}\n"*len(song_artist)).format(*song_artist)
print(song_artist_str)

fave_artists = ['Kendrick Lamar', 'Lil Uzi Vert', 'Migos', 'Childish Gambino',
                'Alessia Cara', 'Rita Ora']

