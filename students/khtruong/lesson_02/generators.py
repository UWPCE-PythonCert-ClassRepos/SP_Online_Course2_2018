#!/usr/bin/env python
import pandas as pd

music = pd.read_csv("featuresdf.csv")
gen = (metadata for metadata in zip(music.artists, music.name)
       if metadata[0] == 'Ed Sheeran')
for g in gen:
    print(f'{g[1]} -- {g[0]}')
