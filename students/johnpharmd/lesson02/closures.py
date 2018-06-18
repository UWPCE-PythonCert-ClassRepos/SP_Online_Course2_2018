import pandas as pd

# Also uses Spotify 2017 top100 track data with Pandas
m = pd.read_csv('featuresdf.csv')


def get_tracks_by_energy(energy=0.1):
    """
    returns tracks by energy, artists, song name
    """
    def find(artists=None, name=None):
        if artists and name:
            tgen = (track for track in zip(m.energy, m.artists, m.name)
                    if track[0] > energy)
            return sorted(list(tgen), reverse=True)
    return find


etracks = get_tracks_by_energy(energy=0.8)
print(etracks(artists=True, name=True))

# Results
"""
(0.932, 'Steve Aoki', 'Just Hold On'),
(0.8759999999999999, 'Ed Sheeran', 'Galway Girl'),
(0.868, 'Maggie Lindemann', 'Pretty Girl - Cheat Codes X CADE Remix'),
(0.8640000000000001, 'Wisin', 'Escápate Conmigo'),
(0.8590000000000001, 'The Chainsmokers', "Don't Let Me Down"),
(0.843, 'Starley', 'Call On Me - Ryan Riback Extended Remix'),
(0.838, 'CNCO', 'Reggaetón Lento (Bailemos)'),
(0.836, 'Martin Jensen', 'Solo Dance'),
(0.8340000000000001, 'Ed Sheeran', 'Castle on the Hill'),
(0.823, 'Enrique Iglesias', 'SUBEME LA RADIO'),
(0.8170000000000001, 'Jason Derulo',
'Swalla (feat. Nicki Minaj & Ty Dolla $ign)'),
(0.815, 'Luis Fonsi', 'Despacito - Remix'),
(0.813, 'The Weeknd', 'I Feel It Coming'),
(0.812, 'Post Malone', 'Congratulations'),
(0.81, 'Imagine Dragons', 'Thunder'),
(0.809, 'The Vamps', 'All Night'),
(0.804, 'Danny Ocean', 'Me Rehúso'),
(0.8029999999999999, 'Bruno Mars', '24K Magic'),
(0.8009999999999999, 'Katy Perry', 'Chained To The Rhythm')]
"""
