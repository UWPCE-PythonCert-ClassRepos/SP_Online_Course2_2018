import pandas as pd

MAX_DANCEABILITY = 0.8
MAX_LOUDNESS = -5
DANCE_NDX = 0
LOUD_NDX = 1
ARTIST_NDX = 2
NAME_NDX = 3

# read in csv file for processing 
music = pd.read_csv("featuresdf.csv")

# combine (zip) music into tuples 
musicZip = zip(music.danceability, music.loudness, music.artists, music.name)

# select songs that meet dancebility and loudness thresholds
songs = [x for x in musicZip if x[DANCE_NDX] > MAX_DANCEABILITY and x[LOUD_NDX] < MAX_LOUDNESS]

# sort by dancebility in descending order
songs.sort(reverse=True)

# print top five danceable songs 
print("{:15} {:43} {:16} {:15}".format("Artist","Name","Danceability","Loudness"))
print("-" *85)

for song in songs[:5]:
    print("{:15} {:35} {:15.1f} {:15.1f}".format(song[ARTIST_NDX], song[NAME_NDX], song[DANCE_NDX], song[LOUD_NDX]))
