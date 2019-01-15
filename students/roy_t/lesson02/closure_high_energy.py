#!/usr/bin/env python3

__author__ = "roy_t  githubtater"

import pandas as pd
music = pd.read_csv('featuresdf.csv')


def my_closure():
	def danceable(danceability=0.8):
		tracks = ((round(dance, 3), artist, song_name)
		          for dance, artist, song_name in zip(music.danceability, music.artists, music.name)
		          if dance >= danceability)
		return tracks
	return danceable


def print_danceables(iterable):
    """Function to print an iterable, including generators"""
    print('Top Danceable Tracks of 2017')
    format_str = '{:<15}{:<20}{:<20}'
    print(format_str.format('Danceability', 'Artist', 'Song'))
    for artist_combo in sorted(iterable, reverse=True):
        print(format_str.format(*artist_combo))
    print('\n')


def main():
	# create the intial generator object
	danceable_tracks = my_closure()
	print_danceables(danceable_tracks())# passing no arguments with danceable_tracks uses default danceability == 0.8

	# Using the same generator object, get danceable tracks over 0.9 by passing the parameter
	print_danceables(danceable_tracks(0.9))


if __name__ == "__main__":
	main()
