'''
Lesson 2 Assignment #1: Generators
'''

import numpy as np
import pandas as pd
music = pd.read_csv("featuresdf.csv")

def get_name(result):
    return result[1]

results = sorted([(a,n) for a,n in zip(music.artists, music.name) if a == "Ed Sheeran"], key=get_name)

def my_generator():
    for i, result in enumerate(results):
        yield result

gen = my_generator()
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))


