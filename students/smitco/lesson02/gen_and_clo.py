# lesson 02 generators and closures
# !/usr/bin/env python3

import pandas as pd
music = pd.read_csv("featuresdf.csv")

def faves_generator():
    gen_info = list(zip(music.name, music.artists))
    favorite = ((x[0], x[1]) for x in gen_info if x[1] == "Ed Sheeran")
    print("My Favorite Top Tracks of 2017\n")
    for f in favorite:
        print("{} by {}".format(*f))

faves_generator()

def energy_closure(level):
    def music_filter():
        clos_info = list(zip(music.name, music.artists, music.energy))
        for r in clos_info:
            if r[2] > level:
                print("{} by {} with {:.3f} Energy".format(*r))
    return music_filter
            
print("\n\nHigh Energy Top Tracks of 2017\n")    
high_energy = energy_closure(0.8)
high_energy()