import pandas as pd
music = pd.read_csv('featuresdf.csv')

#determines the songs that have high energy
def high_energy_chart():
    def high_energy():
        results = [(a, b, c) for a, b, c in zip(music.artists, music.name, music.energy) if c > .8]
        results.sort(key=sort_by_energy, reverse=True)
        return results
    return high_energy
    
#function for sorting the tuples by 3rd element (energy)
def sort_by_energy(i):
    return i[2]

#runs the high_energy function if executable file is run
if __name__ == "__main__":
    high_energy_chart()
    
"""What this generates:
[('Steve Aoki', 'Just Hold On', 0.932),
 ('Ed Sheeran', 'Galway Girl', 0.8759999999999999),
 ('Maggie Lindemann', 'Pretty Girl - Cheat Codes X CADE Remix', 0.868),
 ('Wisin', 'Escápate Conmigo', 0.8640000000000001),
 ('The Chainsmokers', "Don't Let Me Down", 0.8590000000000001),
 ('Starley', 'Call On Me - Ryan Riback Extended Remix', 0.843),
 ('CNCO', 'Reggaetón Lento (Bailemos)', 0.838),
 ('Martin Jensen', 'Solo Dance', 0.836),
 ('Ed Sheeran', 'Castle on the Hill', 0.8340000000000001),
 ('Enrique Iglesias', 'SUBEME LA RADIO', 0.823),
 ('Jason Derulo',
  'Swalla (feat. Nicki Minaj & Ty Dolla $ign)',
  0.8170000000000001),
 ('Luis Fonsi', 'Despacito - Remix', 0.815),
 ('The Weeknd', 'I Feel It Coming', 0.813),
 ('Post Malone', 'Congratulations', 0.812),
 ('Imagine Dragons', 'Thunder', 0.81),
 ('The Vamps', 'All Night', 0.809),
 ('Danny Ocean', 'Me Rehúso', 0.804),
 ('Bruno Mars', '24K Magic', 0.8029999999999999),
 ('Katy Perry', 'Chained To The Rhythm', 0.8009999999999999)]"""