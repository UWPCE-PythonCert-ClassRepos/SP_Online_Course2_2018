def danceable(music_tuple):
    return music_tuple[2]

try:
    import sys
    import pandas as pd
except ModuleNotFoundError:
    print("Must use Python 2 for pandas module")
    sys.exit()

music = pd.read_csv("featuresdf.csv")

dance = [(n, a, d, l)
         for n, a, d, l in
         zip(music.name, music.artists, music.danceability, music.loudness)
         if d > 0.8 and l < -5.0]

#top_dance = sorted(dance, key=(lambda x: x[2]), reverse=True)
top_dance = sorted(dance, key=danceable, reverse=True)
top_dance = [(n, a) for n, a, d, l in top_dance]
top_dance_str = ("{}"+"\n{}"*(len(top_dance)-1)).format(*top_dance)
print(top_dance_str)
with open("top_danceables_2017.txt", 'w+') as spotify:
    spotify.write(top_dance_str)
    


