import pandas as pd

# 1st ex.: Using Spotify 2017 top100 track data w/ Pandas + List Comprehensions
# m = pd.read_csv('featuresdf.csv')
m = pd.read_csv('featuresdf.csv')

print('m.head() returns:\n')
print(m.head())
print('\nm.describe() returns:\n')
print(m.describe(), '\n'*2)

a = sorted(list(zip(m.danceability, m.name, m.artists, m.loudness)),
           reverse=True)
b = [track for track in a if track[0] > 0.8 and track[3] < -5.0]

print('Top 5 tracks in order by descending danceability > 0.8' +
      ' and loudness < -5.0:\n')

for track in b[:5]:
    print(track)
