import pandas as pd

ARTIST_NDX = 0
NAME_NDX = 1

# read in csv file for processing 
music = pd.read_csv("featuresdf.csv")

def songGenerator(artist):
    # combine (zip) music into tuples and select songs that match supplied artist 
    songs = [x for x in zip(music.artists, music.name) if x[ARTIST_NDX] == artist]
    for song in songs:
        yield song

sg = songGenerator("Ed Sheeran")

# print selected artists songs 
print("{:15} {:43}".format("Artist","Name"))
print("-" *45)

while True:
    try:
        # get the next song
        song = next(sg)
        print("{:15} {:35}".format(song[ARTIST_NDX], song[NAME_NDX]))
    except StopIteration:
        # break from loop when StopIteration is raised
        break

