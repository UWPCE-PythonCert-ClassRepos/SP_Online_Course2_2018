import pandas as pd

def top_tracks(threshold):
    def test_tracks(song):
        if song[2] > threshold:
            return song
    return test_tracks


if __name__ == '__main__':
    music = pd.read_csv("featuresdf.csv")
    
    track_list = [x for x in zip(music.name, music.artists, music.energy)]
    
    high_energy_tracks = top_tracks(0.8)
    
    for track in track_list:
        print_song = high_energy_tracks(track)
        if print_song:
            print(print_song)