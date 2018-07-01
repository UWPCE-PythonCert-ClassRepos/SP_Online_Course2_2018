import pandas as pd

def energy(energy):
    def get_energy_tracks():
        music = pd.read_csv("featuresdf.csv")
        return [song for song in zip(music.artists, music.name, music.energy) if song[2] > energy]
    return get_energy_tracks


if __name__ == "__main__":
    energy_8 = energy(0.8)
    for song in energy_8():
        print("{artist}-{song}: {energy}".format(artist=song[0], song=song[1], energy=song[2]))

# Luis Fonsi-Despacito - Remix: 0.815
# Post Malone-Congratulations: 0.812
# Jason Derulo-Swalla (feat. Nicki Minaj & Ty Dolla $ign): 0.8170000000000001
# Ed Sheeran-Castle on the Hill: 0.8340000000000001
# Imagine Dragons-Thunder: 0.81
# Danny Ocean-Me Reh▒so: 0.804
# Ed Sheeran-Galway Girl: 0.8759999999999999
# The Weeknd-I Feel It Coming: 0.813
# Starley-Call On Me - Ryan Riback Extended Remix: 0.843
# Martin Jensen-Solo Dance: 0.836
# Enrique Iglesias-SUBEME LA RADIO: 0.823
# Maggie Lindemann-Pretty Girl - Cheat Codes X CADE Remix: 0.868
# Bruno Mars-24K Magic: 0.8029999999999999
# Katy Perry-Chained To The Rhythm: 0.8009999999999999
# Wisin-Esc▒pate Conmigo: 0.8640000000000001
# Steve Aoki-Just Hold On: 0.932
# CNCO-Reggaet▒n Lento (Bailemos): 0.838
# The Vamps-All Night: 0.809
# The Chainsmokers-Don't Let Me Down: 0.8590000000000001
