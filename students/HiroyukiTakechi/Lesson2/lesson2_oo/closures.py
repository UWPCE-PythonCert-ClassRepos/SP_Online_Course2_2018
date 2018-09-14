'''
Lesson 2 Assignment #2: Closures
'''

import numpy as np
import pandas as pd #this code gives me an error message
music = pd.read_csv("featuresdf.csv")


def closure_1():
    def closure_2():
        for a, t, e in zip(music.artists, music.name, music.energy):
            if e < 0.8:
                print ([a,t,e])
    return closure_2

def main():
    func = closure_1()
    print(func())


if __name__ == "__main__":
    main()