from fave_track_gen import fave_songs_by_artists

def test_kungfu_kenny():
    kdot = fave_songs_by_artists('Kendrick Lamar')
    assert next(kdot) == 'HUMBLE.'
    assert next(kdot) == 'DNA.'

def test_ed_sheeran():
    ed = fave_songs_by_artists('Ed Sheeran')
    assert next(ed) == 'Shape of You'
    assert next(ed) == 'Castle on the Hill'
    assert next(ed) == 'Galway Girl'
    assert next(ed) == 'Perfect'

