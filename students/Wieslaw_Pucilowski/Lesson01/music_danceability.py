import pandas as pd

__author__="Wieslaw Pucilowski"

music = pd.read_csv("featuresdf.csv")


print("{}:\n".format('''TOP 5 Artists and their song
with danceability over 0.8 and loudness below -5.0'''))
for i in sorted([x for x in list(zip(music.name,
                            music.artists,
                            music.danceability,
                            music.loudness))
        if (x[2] > 0.8) & (x[3] < -5.0)],
            key=lambda x: x[2], reverse=True)[:5]:
    print("Artist: {}, Song: {}".format(i[1], i[0]))