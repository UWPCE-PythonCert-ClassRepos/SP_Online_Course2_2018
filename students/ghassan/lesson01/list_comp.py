# editing in order to re-submit lesson1
import pandas as pd


def top_5ive():
    music = pd.read_csv("featuresdf.csv")
    top_five = sorted(
        [(x, y, i, j) for x, y, i, j in zip(
            music.artists, music.name, music.danceability, music.loudness
            ) if i > 0.8 if j < 0.5]
        )[0:5]
    return top_five
