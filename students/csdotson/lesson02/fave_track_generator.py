#!/usr/bin/env python
""" A generator to list favorite artist's tracks """

import pandas as pd
music = pd.read_csv("featuresdf.csv")

tracks = ((x,y) for (x,y) in [(name, artist) for (name, artist) in zip(music.name, music.artists) if artist == "Ed Sheeran"])

for t in tracks:
    print(t)

### Top Ed Sheeran Tracks ###
('Shape of You', 'Ed Sheeran')
('Castle on the Hill', 'Ed Sheeran')
('Galway Girl', 'Ed Sheeran')
('Perfect', 'Ed Sheeran')