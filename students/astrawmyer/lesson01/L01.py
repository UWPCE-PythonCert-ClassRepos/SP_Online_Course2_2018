import pandas as pd
music = pd.read_csv("featuresdf.csv")

song_list = [(artist, song, rating, loud) for (artist, song, rating, loud) in zip(music.artists,music.name,music.danceability,music.loudness) if rating > 0.8 and loud <-5]

song_list = sorted(song_list,key=lambda rate: rate[2], reverse=True)
song_list = song_list[:5]
print(song_list)

"""
[('Migos', 'Bad and Boujee (feat. Lil Uzi Vert)', 0.927, -5.313),
('Drake', 'Fake Love', 0.927, -9.433),
('Kendrick Lamar', 'HUMBLE.', 0.904, -6.8420000000000005),
('21 Savage', 'Bank Account', 0.884, -8.228),
('Jax Jones', "You Don't Know Me - Radio Edit", 0.8759999999999999, -6.053999999999999)]
"""