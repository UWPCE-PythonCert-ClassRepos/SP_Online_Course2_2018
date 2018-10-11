#!/usr/bin/env python3

import pandas as pd

def create_energetic_track_finder(energy):
    ''' Find tracks by energy level '''
    def energetic_tracks(music):
        return [x for x in zip(music.energy, music.artists, music.name) if x[0] >= energy]
    return energetic_tracks

if __name__ == '__main__':
    music = pd.read_csv("featuresdf.csv")
    find_high_energy = create_energetic_track_finder(0.8)
    for track in find_high_energy(music):
        print(f"Track: {track[2]:<45} Artist: {track[1]:<20} Energy: {track[0]:<20.3f}")

'''
Results:
Track: Despacito - Remix                             Artist: Luis Fonsi           Energy: 0.815
Track: Congratulations                               Artist: Post Malone          Energy: 0.812
Track: Swalla (feat. Nicki Minaj & Ty Dolla $ign)    Artist: Jason Derulo         Energy: 0.817
Track: Castle on the Hill                            Artist: Ed Sheeran           Energy: 0.834
Track: Thunder                                       Artist: Imagine Dragons      Energy: 0.810
Track: There's Nothing Holdin' Me Back               Artist: Shawn Mendes         Energy: 0.800
Track: Me Reh▒so                                     Artist: Danny Ocean          Energy: 0.804
Track: Galway Girl                                   Artist: Ed Sheeran           Energy: 0.876
Track: I Feel It Coming                              Artist: The Weeknd           Energy: 0.813
Track: Call On Me - Ryan Riback Extended Remix       Artist: Starley              Energy: 0.843
Track: Solo Dance                                    Artist: Martin Jensen        Energy: 0.836
Track: SUBEME LA RADIO                               Artist: Enrique Iglesias     Energy: 0.823
Track: Pretty Girl - Cheat Codes X CADE Remix        Artist: Maggie Lindemann     Energy: 0.868
Track: 24K Magic                                     Artist: Bruno Mars           Energy: 0.803
Track: Chained To The Rhythm                         Artist: Katy Perry           Energy: 0.801
Track: Esc▒pate Conmigo                              Artist: Wisin                Energy: 0.864
Track: Just Hold On                                  Artist: Steve Aoki           Energy: 0.932
Track: Reggaet▒n Lento (Bailemos)                    Artist: CNCO                 Energy: 0.838
Track: All Night                                     Artist: The Vamps            Energy: 0.809
Track: Don't Let Me Down                             Artist: The Chainsmokers     Energy: 0.859
'''