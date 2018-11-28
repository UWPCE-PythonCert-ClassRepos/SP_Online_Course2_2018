import pandas as pd
music = pd.read_csv("featuresdf.csv")

danceability = [x for x in music.danceability if x > 0.8]
print(danceability)