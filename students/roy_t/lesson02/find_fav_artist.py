#!/usr/bin/env python3

import pandas as pd
import pprint
from itertools import count, tee

music = pd.read_csv('featuresdf.csv')


def find_favorite_artist(fav_artist):
    """Return tee of two identical generators of fav_artists songs from 2017"""
    favorites = ((artist, song_name)
                for artist, song_name in zip(music.artists, music.name)
                if fav_artist.lower() in artist.lower())
    return favorites


def gen_len(iterable):
    total = sum(1 for i in iterable)
    return total


def print_favorites(iterable, title='Top Songs of 2017'):
    """Function to print an iterable, including generators"""
    print(title)
    format_str = '{:<20}{:<20}'
    print(format_str.format('Artist(s)', 'Song'))
    for artist_combo in iterable:
        print(format_str.format(*artist_combo))
    print('\n')


def main():
    while True:
        # Ask the user who their favorite artist is
        fav_input = input('Enter your favorite artist: ')
        # We have to have something to search for. If not, ask again.
        if fav_input == '':
            print('Entry cannot be blank.\n')
            continue

        # tee object containing two identical generators of search results from above
        find_favs = find_favorite_artist(fav_input)
        find_favs_tee = tee(find_favs, 2)
        count_gen = find_favs_tee[0]
        print_gen = find_favs_tee[1]
        total = gen_len(count_gen)
        if total == 0:
            print('Your favorite artist wasn\'t found.\nBut, you\'re in luck, because everyone loves Ed Sheeran!!')
            print_favorites(find_favorite_artist('Ed Sheeran'))
        else:
            print_favorites(print_gen)


if __name__ == "__main__":
    main()
