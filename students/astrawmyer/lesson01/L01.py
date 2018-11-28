import pandas as pd
music = pd.read_csv("featuresdf.csv")

song_list = [(artist, song, rating, loud) for (artist, song, rating, loud) in zip(music.artists,music.name,music.danceability,music.loudness) if rating > 0.8 and loud <-5]
print(song_list)

print(sorted(song_list,key=lambda rate: rate[2]))