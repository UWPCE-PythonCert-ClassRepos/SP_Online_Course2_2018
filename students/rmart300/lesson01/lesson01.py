import pandas as pd

music = pd.read_csv('featuresdf.csv')

"""
Your job, now, is to get artists and song names for for tracks with danceability scores over 0.8 and loudness scores below -5.0. In other words, quiet yet danceable tracks. Also, these tracks should be sorted in descending order by danceability so that the most danceable tracks are up top
"""

names = [x for x in music.name]
artists = [x for x in music.artists]
danceable_scores = [x for x in music.danceability]
quiet_scores = [x for x in music.loudness]

all_songs = zip(names, artists, danceable_scores, quiet_scores)

filtered_songs = [x for x in list(all_songs) if x[2] > 0.8 and x[3] < -5.0]

for song in sorted(filtered_songs, key=lambda x:x[2], reverse=True):
    print("{:40} {:30} {:20} {:20}".format(song[0],song[1],str(song[2]),str(song[3])))

