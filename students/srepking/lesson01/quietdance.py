import pandas as pd
music = pd.read_csv("featuresdf.csv")


qualified = [(artist, song, danceability, loudness)
                  for artist, song, danceability, loudness
                  in zip(music.artists,music.name,music.danceability,music.loudness)
                  if (danceability > 0.8 and loudness < -5.0)]
qualified_sorted=sorted(qualified,key= lambda sort_by: sort_by[2], reverse=True)
print(qualified_sorted)



