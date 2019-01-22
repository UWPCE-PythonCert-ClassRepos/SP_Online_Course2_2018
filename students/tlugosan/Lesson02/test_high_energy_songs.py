#!/usr/bin/env python3

import pytest
import high_energy_songs_closure as hes

def test_high_energy_songs():
    t1 = hes.high_energy_songs(0.8)
    assert t1('Ed Sheeran') == [('Ed Sheeran', 'Castle on the Hill', 0.8340000000000001),
 ('Ed Sheeran', 'Galway Girl', 0.8759999999999999)]
    assert t1('Luis Fonsi') == [('Luis Fonsi', 'Despacito - Remix', 0.815)]


def test_high_energy_songs():
    t2 = hes.high_energy_songs(0.2)
    assert t2('Ed Sheeran') == [('Ed Sheeran', 'Shape of You', 0.652),
 ('Ed Sheeran', 'Castle on the Hill', 0.8340000000000001),
 ('Ed Sheeran', 'Galway Girl', 0.8759999999999999),
 ('Ed Sheeran', 'Perfect', 0.44799999999999995)]
    assert t2('Luis Fonsi') == [('Luis Fonsi', 'Despacito - Remix', 0.815),
 ('Luis Fonsi', 'Despacito (Featuring Daddy Yankee)', 0.7859999999999999)]
