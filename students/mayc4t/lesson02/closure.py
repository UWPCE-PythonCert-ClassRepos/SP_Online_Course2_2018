#!/usr/bin/env python3

# FileID: closure.py
#   Using the same data set, write a closure to capture high energy tracks.
#   We will define high energy tracks as anything over 0.8.
#   Submit your code and the tracks it finds, artist name, track name and
#   energy value.

import pandas as pd

music_db = pd.read_csv("featuresdf.csv")


def music_finder(val):
    # generate the list
    ml = [x for x in zip(music_db.artists, music_db.name, music_db.energy)]

    def track_list(val):
        for track in ml:
            if track[2] > val:
                yield (track)
    return track_list(val)


he_ml = music_finder(0.8)
for each_track in he_ml:
    print (each_track)
