import pandas as pd

# 1st ex.: Using Spotify 2017 top100 track data w/ Pandas + List Comprehensions
m = pd.read_csv('featuresdf.csv')

print('m.head() returns:\n')
print(m.head())
print('\nm.describe() returns:\n')
print(m.describe(), '\n'*2)

# dance = [x for x in music.danceability if x > 0.8]
# quiet = [y for y in music.loudness if y < -5.0]
# artists = [a for a in music.artists]
# songs = [s for s in music.name]

# quiet_dance = list(zip(quiet, sorted(dance, reverse=True)))
# artists_songs = list(zip(artists, songs))

# print(list(zip(artists_songs, quiet_dance))[:5])

print('Top 5 tracks in descending order by danceability > 0.8' +
      ' and loudness < -5.0:\n')

a = sorted(list(zip(m.danceability, m.name, m.artists, m.loudness)),
           reverse=True)
b = [track for track in a if track[3] < -5.0]

for track in b[:5]:
    print(track)
