#-------------------------------------------------#
# Title: Dance Songs
# Dev:   LDenney
# Date:  February 3rd, 2019
# ChangeLog: (Who, When, What)
#   Laura Denney, 2/3/19, Started work on dance songs
#-------------------------------------------------#


'''id', 'name', 'artists', 'danceability', 'energy', 'key',
       'loudness', 'mode', 'speechiness', 'acousticness',
       'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms',
       'time_signature'
'''

import pandas as pd
music = pd.read_csv("featuresdf.csv")

def is_quiet_dancy(loudness,danceability):
    return loudness < -5.0 and danceability > 0.8

all_songs = sorted(list(zip(music.name, music.artists, music.danceability,music.loudness)),key = lambda x:x[2],reverse=True)

dance_songs = [(name,artists) for name, artists, danceability, loudness in all_songs if is_quiet_dancy(loudness,danceability)]

top_5dance = dance_songs[:5]

str_dance = '''
Most Danceable Quiet Dance Songs 2017| Artist
---------------------------------------------'''
strformat = '\n{:<40}{:<13}'
for name,artist in dance_songs:
    str_dance +=  strformat.format(name, artist)

print(str_dance)


