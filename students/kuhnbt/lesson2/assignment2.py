%cd C:/Users/kuhnb/pythoncourse2/SP_Online_Course2_2018/students/kuhnbt/lesson1
import pandas as pd

# Problem 1

df = pd.read_csv('featuresdf.csv')
sheeran_songs = list(df[df['artists']=='Ed Sheeran']['name'])
sheeran_generator = (song for song in sheeran_songs)
print([song for song in sheeran_generator])

# Problem 2

def get_high_energy_tracks(cutoff):
    energy_cutoff = cutoff
    def get_track_info(df):
        tracks = df[df['energy']>energy_cutoff]
        return tracks[['name','artists','energy']]
    return get_track_info

high_energy = get_high_energy_tracks(.8)
print(high_energy(df))