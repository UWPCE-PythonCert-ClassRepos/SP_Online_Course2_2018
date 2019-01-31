#!/usr/bin/env python
import pandas as pd
music = pd.read_csv("featuresdf.csv")
#Method one:
def tracks():
    high_energy_tracks = [song for song in zip(music.name, music.artists, music.energy) if song[2] > 0.8]
    def inner_func():
        print("The high energy tracks are:")
        print("{:<43}{:<20}{:<20}".format("Name", "Artist", "Energy"))
        for track in high_energy_tracks:
            print("{:<43}{:<20}{:<20}".format(track[0],track[1],track[2]))
    return inner_func

result = tracks()


#Method two:
def tracks_two():
    def inner_func_two():
        print("The high energy tracks are:")
        print("{:<43}{:<20}{:<20}".format("Name", "Artist", "Energy"))
        for track in list(zip(music.name, music.artists, music.energy)):
            if track[2] > 0.8:
                print("{:<43}{:<20}{:<20}".format(track[0],track[1],track[2]))
    return inner_func_two

result_two = tracks_two()


if __name__ == "__main__":
    result()
    # result_two()
