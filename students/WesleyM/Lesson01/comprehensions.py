import pandas as pd
music = pd.read_csv("featuresdf.csv")

result = sorted([x for x in
          zip(music.artists, music.name, music.danceability, music.loudness)
          if x[2] > 0.8 and x[3] < - 5.0], key = lambda x:x[2], reverse=True)

for names in result[:5]:
    print(names[0], "-", names[1])
    
