import pandas as pd
music = pd.read_csv("featuresdf.csv")

song_list = [(x,y) for (x,y) in zip(music.name,music.danceability) if y > 0.8]
print(song_list)