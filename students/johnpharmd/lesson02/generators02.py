import pandas as pd

# Again uses Spotify 2017 top100 track data and Pandas, but with generator
# expression instead of list comprehension this time

m = pd.read_csv('featuresdf.csv')

trackgen = (track for track in zip(m.name, m.artists)
                if track[1] == 'Ed Sheeran')

for track in trackgen:
    print(track)

# returns
# ('Shape of You', 'Ed Sheeran')
# ('Castle on the Hill', 'Ed Sheeran')
# ('Galway Girl', 'Ed Sheeran')
# ('Perfect', 'Ed Sheeran')
