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
from timeit import timeit as timer
import pandas as pd
music = pd.read_csv("featuresdf.csv")

repetitions = 10000000
all_songs = []

comprehension1 = [(name,artists) for name, artists, danceability, loudness in all_songs if is_quiet_dancy(loudness,danceability)]
comprehension2 = [(name, artists) for name, artists, danceability, loudness in all_songs if (loudness < -5.0 and danceability > 0.8)]
comprehension3 = [(lambda x,y: (x, y))(x,y) for x,y,z,a in all_songs if (lambda a,z:(a < -5.0 and z> 0.8))(a,z)]

def is_quiet_dancy(loudness,danceability):
    return loudness < -5.0 and danceability > 0.8

def main(test_comprehension):
    all_songs = sorted(list(zip(music.name, music.artists, music.danceability,music.loudness)),key = lambda x:x[2],reverse=True)

    dance_songs = test_comprehension

    top_5dance = dance_songs[:5]

    str_dance = '''
Most Danceable Quiet Dance Songs 2017| Artist
---------------------------------------------'''
    strformat = '\n{:<40}{:<13}'
    for name,artist in dance_songs:
        str_dance +=  strformat.format(name, artist)

    print(str_dance)


if __name__ == '__main__':
    print('\ncomp1')
    print(timer('comprehension1 = [(name,artists) for name, artists, danceability, loudness in all_songs if is_quiet_dancy(loudness,danceability)]',
                globals=globals(), number = repetitions))
    print('\ncomp2')
    print(timer('comprehension2 = [(name, artists) for name, artists, danceability, loudness in all_songs if (loudness < -5.0 and danceability > 0.8)]',
                globals=globals(), number = repetitions))
    print('\ncomp3')
    print(timer('comprehension3 = [(lambda x,y: (x, y))(x,y) for x,y,z,a in all_songs if (lambda a,z:(a < -5.0 and z> 0.8))(a,z)]',
                globals=globals(), number = repetitions))