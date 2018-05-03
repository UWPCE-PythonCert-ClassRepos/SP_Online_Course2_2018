#!/usr/bin/env python3

import pandas as pd


def high_energy(music):
    def find_high_energy():
        print(
            [(x, y, z) for x, y, z in zip(
                music.artists, music.name, music.energy
                ) if z > 0.8]
        )
    return find_high_energy()


def main():
    music = pd.read_csv("featuresdf.csv")
    high_energy(music)


if __name__ == '__main__':
    main()
