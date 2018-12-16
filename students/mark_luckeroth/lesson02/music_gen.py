#!/usr/bin/env python3
import pandas as pd


def songs_by(data, singer):
    return ((song, artist) for song, artist in zip(data.name, data.artists)
            if artist == singer)


if __name__ == '__main__':
    singer = 'Ed Sheeran'
    music = pd.read_csv("featuresdf.csv")
    song_gen = songs_by(music, singer)
    for n in song_gen:
        print('Song Name: {}, performed by: {}'.format(*n))
