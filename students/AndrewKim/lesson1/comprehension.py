#!/usr/bin/env python3

import pandas as pd

music = pd.read_csv("featuresdf.csv")

def get_danc(elem):
	return elem[2]


result = sorted([x for x in zip(music.artists, music.name, music.danceability, music.loudness) 
				if x[2] > 0.8 and x[3] < -5.0], 
				key=get_danc, 
				reverse=True)[:5]

	
print(result)