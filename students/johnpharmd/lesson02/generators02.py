import pandas as pd

# Again uses Spotify 2017 top100 track data and Pandas, but with generator
# expression and generator function instead of list comprehension this time

m = pd.read_csv('featuresdf.csv')


def find_tracks():
    """
    returns all Ed Sheeran tracks, one by one
    """
    trackgen = (track for track in zip(m.name, m.artists)
                      if track[1] == 'Ed Sheeran')
    while True:
        for track in trackgen:
            yield track
