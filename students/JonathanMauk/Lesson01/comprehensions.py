import pandas as pd

music = pd.read_csv("featuresdf.csv")

song_list = [x for x in zip(music.danceability, music.loudness, music.name, music.artists)
             if x[0] > 0.8 and x[1] < -5]

quiet_and_danceable = sorted(song_list, reverse=True)

print("Type five songs by danceability with loudness less than -5:\n")
number = 1
for x in quiet_and_danceable[:5]:
    print(str(number) + ". " + x[2] + "\n   by " + x[3] + "\n   (Danceability: " + str(x[0]) + ")\n")
    number = number + 1
