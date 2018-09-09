# Nebiat Abraha 
# Comprehensions


import pandas as pd
music = pd.read_csv("featuresdf.csv")

dance = music['name'][music['danceability'] > .8][music['loudness'] < -5]
dance.head(5)

# Top 5 songs: 
# HUMBLE.
# Mask off
# Passionfruit
# Strip that Down
# Bad and Boujee