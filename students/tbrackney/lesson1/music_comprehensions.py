#!/usr/bin/env python3
"""
File Name: music_comprehension.py
Author: Travis Brackney
Class: Python 220 - Self paced online
Date Created 1/14/2019
Python Version: 3.6.4
"""

import pandas as pd

music = pd.read_csv("featuresdf.csv")

soft_bangers = [(n, a, d, l) for n, a, d, l in zip(music.name, music.artists, music.danceability, music.loudness) if d > 0.8 and l < -5.0]
soft_bangers.sort(key=lambda track: track[2], reverse=True)

for x in range(5):
    print(soft_bangers[x])
