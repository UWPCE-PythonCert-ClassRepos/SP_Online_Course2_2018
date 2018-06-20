#!/usr/bin/env python
""" A closure that captures list of high energy tracks """

import pandas as pd
music = pd.read_csv("featuresdf.csv")

# Closure
def energy_track_finder(e):
    def find_tracks():
        return [(name, artist, energy) for (name, artist, energy) in zip(music.name, music.artists, music.energy) if energy > e]
    return find_tracks

# List of tracks returned - name, artist, and energy value
[('Despacito - Remix', 'Luis Fonsi', 0.815),
 ('Congratulations', 'Post Malone', 0.812),
 ('Swalla (feat. Nicki Minaj & Ty Dolla $ign)',
  'Jason Derulo', 0.8170000000000001),
 ('Castle on the Hill', 'Ed Sheeran', 0.8340000000000001),
 ('Thunder', 'Imagine Dragons', 0.81),
 ('Me Rehúso', 'Danny Ocean', 0.804),
 ('Galway Girl', 'Ed Sheeran', 0.8759999999999999),
 ('I Feel It Coming', 'The Weeknd', 0.813),
 ('Call On Me - Ryan Riback Extended Remix', 'Starley', 0.843),
 ('Solo Dance', 'Martin Jensen', 0.836),
 ('SUBEME LA RADIO', 'Enrique Iglesias', 0.823),
 ('Pretty Girl - Cheat Codes X CADE Remix', 'Maggie Lindemann', 0.868),
 ('24K Magic', 'Bruno Mars', 0.8029999999999999),
 ('Chained To The Rhythm', 'Katy Perry', 0.8009999999999999),
 ('Escápate Conmigo', 'Wisin', 0.8640000000000001),
 ('Just Hold On', 'Steve Aoki', 0.932),
 ('Reggaetón Lento (Bailemos)', 'CNCO', 0.838),
 ('All Night', 'The Vamps', 0.809),
 ("Don't Let Me Down", 'The Chainsmokers', 0.8590000000000001)]