import pandas as pd


def songs_by_energy(energy=0.8):  # Default value is 0.8 to get high energy songs, but can be defined by user.
    def find_songs(song_list):
        return [song for song in zip(song_list.artists, song_list.name, song_list.energy) if song[2] > energy]
    return find_songs


music = pd.read_csv("featuresdf.csv")
high_energy_list = songs_by_energy()  # Using default value of 0.8.
high_energy_query = high_energy_list(music)  # Running data set through our closure.

for songs in high_energy_query:
    print(f"-   Artist: {songs[0]}\n\tTitle: {songs[1]}\n\tEnergy: {songs[2]}")

# The above for-loop should give these results:
#
# -   Artist: Luis Fonsi
# 	Title: Despacito - Remix
# 	Energy: 0.815
# -   Artist: Post Malone
# 	Title: Congratulations
# 	Energy: 0.812
# -   Artist: Jason Derulo
# 	Title: Swalla (feat. Nicki Minaj & Ty Dolla $ign)
# 	Energy: 0.8170000000000001
# -   Artist: Ed Sheeran
# 	Title: Castle on the Hill
# 	Energy: 0.8340000000000001
# -   Artist: Imagine Dragons
# 	Title: Thunder
# 	Energy: 0.81
# -   Artist: Danny Ocean
# 	Title: Me Rehúso
# 	Energy: 0.804
# -   Artist: Ed Sheeran
# 	Title: Galway Girl
# 	Energy: 0.8759999999999999
# -   Artist: The Weeknd
# 	Title: I Feel It Coming
# 	Energy: 0.813
# -   Artist: Starley
# 	Title: Call On Me - Ryan Riback Extended Remix
# 	Energy: 0.843
# -   Artist: Martin Jensen
# 	Title: Solo Dance
# 	Energy: 0.836
# -   Artist: Enrique Iglesias
# 	Title: SUBEME LA RADIO
# 	Energy: 0.823
# -   Artist: Maggie Lindemann
# 	Title: Pretty Girl - Cheat Codes X CADE Remix
# 	Energy: 0.868
# -   Artist: Bruno Mars
# 	Title: 24K Magic
# 	Energy: 0.8029999999999999
# -   Artist: Katy Perry
# 	Title: Chained To The Rhythm
# 	Energy: 0.8009999999999999
# -   Artist: Wisin
# 	Title: Escápate Conmigo
# 	Energy: 0.8640000000000001
# -   Artist: Steve Aoki
# 	Title: Just Hold On
# 	Energy: 0.932
# -   Artist: CNCO
# 	Title: Reggaetón Lento (Bailemos)
# 	Energy: 0.838
# -   Artist: The Vamps
# 	Title: All Night
# 	Energy: 0.809
# -   Artist: The Chainsmokers
# 	Title: Don't Let Me Down
# 	Energy: 0.8590000000000001
