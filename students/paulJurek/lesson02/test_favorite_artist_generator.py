"""tests the favorite artist generator as part of lesson02"""
import pytest

from favorite_artist_generator import get_artist_tracks


def test_get_eds_songs():
    """this tests that the song names from Ed Sheeran are returned from generator"""
    expected_results = {'Shape of You', 'Castle on the Hill', 'Galway Girl', 'Perfect'}
    actual_resaults = get_artist_tracks(artist='Ed Sheeran', 
                          filename=r'lesson02\top-tracks-of-2017.csv')
    assert expected_results == set(actual_resaults)
