#!/usr/bin/env python3
import pandas as pd


def make_upper_att_filter(att, value):
    def att_filter(data):
        return [(song, artist, attribute) for song, artist, attribute
                in zip(data.name, data.artists, data[att])
                if attribute > value]
    return att_filter


if __name__ == '__main__':
    attribute = 'energy'
    min_value = 0.8
    music = pd.read_csv("featuresdf.csv")
    energy_filter = make_upper_att_filter(attribute, min_value)
    for n in energy_filter(music):
        print('Song Name: {}, performed by: {}, energy value: {}'.format(*n))