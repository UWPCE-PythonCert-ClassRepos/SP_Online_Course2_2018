#!/usr/bin/env python3

import pandas as pd

"""
Lesson2 - Generators & Closures
"""

music = pd.read_csv("featuresdf.csv")


def gen_track(music=zip(music.artists, music.name), artist='Ed Sheeran'):
    """
    'Shape of You by Ed Sheeran'
    'Castle on the Hill by Ed Sheeran'
    'Galway Girl by Ed Sheeran'
    'Perfect by Ed Sheeran'
    """
    for x in music:
        if x[0] == artist:
            yield f'{x[1]} by {x[0]}'


def energy_tracks(music=zip(music.artists, music.name, music.energy)):
    """
    'Despacito - Remix by Luis Fonsi | Energy: 0.815'
    'Congratulations by Post Malone | Energy: 0.812'
    'Swalla (feat. Nicki Minaj & Ty Dolla $ign) by Jason Derulo | Energy: 0.8170000000000001'
    'Castle on the Hill by Ed Sheeran | Energy: 0.8340000000000001'
    'Thunder by Imagine Dragons | Energy: 0.81'
    'Me Rehúso by Danny Ocean | Energy: 0.804'
    'Galway Girl by Ed Sheeran | Energy: 0.8759999999999999'
    'I Feel It Coming by The Weeknd | Energy: 0.813'
    'Call On Me - Ryan Riback Extended Remix by Starley | Energy: 0.843'
    'Solo Dance by Martin Jensen | Energy: 0.836'
    'SUBEME LA RADIO by Enrique Iglesias | Energy: 0.823'
    'Pretty Girl - Cheat Codes X CADE Remix by Maggie Lindemann | Energy: 0.868'
    '24K Magic by Bruno Mars | Energy: 0.8029999999999999'
    'Chained To The Rhythm by Katy Perry | Energy: 0.8009999999999999'
    'Escápate Conmigo by Wisin | Energy: 0.8640000000000001'
    'Just Hold On by Steve Aoki | Energy: 0.932'
    'Reggaetón Lento (Bailemos) by CNCO | Energy: 0.838'
    'All Night by The Vamps | Energy: 0.809'
    "Don't Let Me Down by The Chainsmokers | Energy: 0.8590000000000001"
    """
    def is_high():
        for x in music:
            if x[2] > 0.8:
                return f'{x[1]} by {x[0]} | Energy: {x[2]}'
    return is_high
