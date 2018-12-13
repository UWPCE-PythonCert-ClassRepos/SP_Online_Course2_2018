#!/usr/bin/env python3

import pandas as pd
from operator import itemgetter

def top_danceability(music):
    danceable = [(a, b, y, z) for a, b, y, z in zip(music.name, music.artists,
                                                    music.danceability,
                                                    music.loudness) if y>0.8 and z<-5.]
    top_danceable = sorted(danceable, key=itemgetter(2), reverse=True)
    return top_danceable[:5]


def pretty_report(data):
    title_str = '{:<40s}|{:^20}|{:^14}|{:^10}'
    bar_str = '-'*87
    entry_str = '{:<40s}|{:^20s}|{:>14.2f}|{:>10.2f}'
    report = [title_str.format('Song Name', 'Artist',
                               'Danceability', 'Loudness'), bar_str]
    for song in data:
        report.append(entry_str.format(*song))
    for line in report:
        print(line)

if __name__ == '__main__':
    music = pd.read_csv("featuresdf.csv")
    top_songs = top_danceability(music)
    pretty_report(top_songs)
