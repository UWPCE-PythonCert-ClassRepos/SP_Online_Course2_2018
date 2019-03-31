import pandas as pd
import itertools

def sort_key(tup):
    """Takes a tuple of at least 3 elements and returns the 2th element."""
    return tup[2]

music = pd.read_csv("featuresdf.csv")

# Create a list of tuples containing songs with danceability > 0.8 and
# loudness < -5
m_filter = [(x, y, z, a) for x,y,z,a in zip(music.name, music.artists,
    music.danceability, music.loudness) if z > 0.8 and a < -5]

# Use the sort_key function to sort by danceability
m_filter = sorted(m_filter, key=sort_key, reverse=True)

field_size = (
    max(len(x[0]) for x in m_filter),
    max(len(x[1]) for x in m_filter),
    len('Danceability'),
    len('Loudness')
    )

# Print a header, followed by table rows
print('{:{}} {:{}} {:{}} {:{}}'.format(*tuple(itertools.chain(*zip(
    ['Title', 'Artists', 'Danceability', 'Loudness'], field_size)))))
for row in m_filter:
    print('{:{}} {:{}} {:<{}.2f} {:<{}.2f}'.format(*tuple(itertools.chain(*zip(row, field_size)))))
