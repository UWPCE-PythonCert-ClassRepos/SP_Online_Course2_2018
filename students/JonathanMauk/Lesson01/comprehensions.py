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

'''
Top five songs, per the above code:

1. Bad and Boujee (feat. Lil Uzi Vert)
   by Migos
   (Danceability: 0.927)

2. Fake Love
   by Drake
   (Danceability: 0.927)

3. HUMBLE.
   by Kendrick Lamar
   (Danceability: 0.904)

4. Bank Account
   by 21 Savage
   (Danceability: 0.884)

5. You Don't Know Me - Radio Edit
   by Jax Jones
   (Danceability: 0.8759999999999999)
'''