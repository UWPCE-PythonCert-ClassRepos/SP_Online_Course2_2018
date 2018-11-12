import pandas as pd
music = pd.read_csv('featuresdf.csv')

def gen_artist_tracks(artist='Ed Sheeran'):
    music_zip = zip(music.name, music.artists)
    for i in music_zip:
        if i[1] == artist:
            yield print(i[1], '-', i[0])


def high_energy(music_file=music):
    def get_next_track(energy_level):
        music_zip = zip(music_file.artists, music_file.name, music_file.energy)
        high_energy_tracks = []
        for i in music_zip:
            if i[2] > energy_level:
                high_energy_tracks.append(i)
        return high_energy_tracks
    return get_next_track
