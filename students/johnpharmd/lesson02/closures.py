import pandas as pd

# Also uses Spotify 2017 top100 track data with Pandas
m = pd.read_csv('featuresdf.csv')


def get_tracks_by_energy(energy):
    """
    returns tracks by artists, song name, energy level
    """
    def find(artists=None, name=None):
        if artists and name:
            tlist = [track for track in zip(m.artists, m.name, m.energy)
                     if m.energy > energy]
            return tlist
    return find


etracks = get_tracks_by_energy(8.0)
print(etracks(artists=True, name=True))
