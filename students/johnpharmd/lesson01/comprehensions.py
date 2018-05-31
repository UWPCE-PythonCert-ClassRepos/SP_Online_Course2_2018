import pandas as pd

# 1st ex.: Using Spotify 2017 top100 track data w/ Pandas + List Comprehensions
music = pd.read_csv('featuresdf.csv')

print('music.head() returns:')
print(music.head())
print('\nmusic.describe() returns:')
print(music.describe(), '\n')

dance = [x for x in music.danceability if x > 0.8]
quiet = [y for y in music.loudness if y < -5.0]
artists = [a for a in music.artists]
songs = [s for s in music.name]

quiet_dance = list(zip(quiet, sorted(dance, reverse=True)))
artists_songs = list(zip(artists, songs))

print('Top 5 tracks by danceability:')
print(list(zip(artists_songs, quiet_dance))[:5])
