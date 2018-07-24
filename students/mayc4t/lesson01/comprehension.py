#!/usr/bin/python 

import pandas as pd
import pandas as pd

music = pd.read_csv("featuresdf.csv")
ml = [x for x in zip(music.name, music.artists, music.danceability, music.loudness) if x[2]>0.8 and x[3]<-5]

# use sort instead of sorted .. --> sort does not return a list, it sorts the list itself
ml.sort(key=lambda x:x[2], reverse=True)
print ("\n\tmusic.name\tmusic.artist\tdanceability > 0.8\tloudness < -5.0", "\n\t", "**"*30)
for top_song in ml[0:5]: print("\t", top_song)


