import pandas as pd

music = pd.read_csv("featuresdf.csv")

print(music.head())
print(music.describe())

dancing_songs = [x for x in zip(music.name, music.danceability, music.loudness) if x[1] > 0.8 and x[2] < -5]

def get_danceability(d):
    return d[1]

my_songs = sorted(dancing_songs, key=get_danceability, reverse=True)

print("Quiet, yet danceable, songs:")
for s in my_songs[0:5]:
    print(s[0])
