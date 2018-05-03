#!/usr/bin/env python3
import pandas as pd


music = pd.read_csv("featuresdf.csv")


def musik():
    total = music['artists'].count()
    count = 0
    while count < total:
        yield (music.artists.iloc[count], music.name.iloc[count])
        count += 1


def main():
    all_artists = musik()
    for item in all_artists:
        if 'Ed Sheeran' in item[0]:
            print(item)


if __name__ == '__main__':
    main()
