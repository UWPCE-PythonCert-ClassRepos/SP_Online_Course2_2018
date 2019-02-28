import pandas as pd

# Read in Spotify's top 100 songs
music = pd.read_csv("featuresdf.csv")

def sheeran_songs(df):
    """Generator returns Ed Sheeran songs from the provided dataframe."""
    for title, artists in zip(df.name, df.artists):
        if 'Ed Sheeran' in artists:
            yield title

# Print Ed Sheeran songs with header
print('Ed Sheeran Songs From the Spotify Top 100 List')
for song in sheeran_songs(music):
    print(song)


def make_energy_limit(df, energy_limit):
    """
    Closure returns a function that generates songs above the specified
    energy level.
    """
    def energy_above():
        nonlocal df
        nonlocal energy_limit
        for title, artists, energy in zip(df.name, df.artists, df.energy):
            if energy > energy_limit:
                yield title, artists, energy
    return energy_above

# Create generator for songs with energy above 0.8
energy_fun = make_energy_limit(music, 0.8)

# Print songs with energy above 0.8 with header
print('\n\nSpotify Top 100 Songs with Energy > 0.8')
for title, artists, energy in energy_fun():
    print('{}, {}, {:.2f}'.format(title, artists, energy))
