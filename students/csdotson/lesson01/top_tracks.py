import pandas as pd
music = pd.read_csv("featuresdf.csv")

### Using Pandas ###
quietly_danceable = music[music.danceability > 0.8][music.loudness < -5.0]

top_five = quietly_danceable.sort_values(by='danceability', ascending=False)[:5]

print(top_five)


### Using Comprehensions ### 
filtered_list = [(name, artist, dance, loud) for (name, artist, dance, loud) in zip(music.name, music.artists, music.danceability, music.loudness) if dance > 0.8 and loud < -5.0]

print(sorted(filtered_list, key=lambda song: song[2], reverse=True)[:5])


### Top Five Songs ###
[('Bad and Boujee (feat. Lil Uzi Vert)', 'Migos', 0.927, -5.313),
 ('Fake Love', 'Drake', 0.927, -9.433),
 ('HUMBLE.', 'Kendrick Lamar', 0.904, -6.842),
 ('Bank Account', '21 Savage', 0.884, -8.228),
 ("You Don't Know Me - Radio Edit", 'Jax Jones', 0.876, -6.054)]