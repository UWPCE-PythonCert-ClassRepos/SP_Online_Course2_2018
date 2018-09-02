import pandas as pd

music = pd.read_csv("featuresdf.csv")


def srt(val):
    return val[3]


data = sorted(list(zip(music.artists, music.name, music.loudness, music.danceability)), key=srt, reverse=True)


print("{:<35} | {:<14}".format("Track Name", "Artist", "Loudness", "Danceability"))
print("----------------------------------------------------------")
[print("{:<35} | {:<14}".format(x[1], x[0], x[2], x[3])) for x in data if x[3] > 0.8 and x[2] < -5.0]
