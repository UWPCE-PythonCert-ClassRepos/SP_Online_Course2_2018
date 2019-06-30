"""
Last week we looked at Spotify’s top tracks from 2017. We used comprehensions and perhaps a lambda to find tracks we might like. 
Having recovered from last week’s adventure in pop music we’re ready to venture back.

Write a generator to find and print all of your favorite artist’s tracks from the data set. 
Your favorite artist isn’t represented in that set? In that case, find Ed Sheeran’s tracks.

Load the data set following the instructions from last week. Submit your generator expression and the titles of your or Ed’s tracks.
"""

import pandas as pd 

music = pd.read_csv("C:\\Users\\Jared\\Documents\\python_220\\SP_Online_Course2_2018\\students\\jared_mulholland\\lesson_1\\featuresdf.csv")

def music_gen(artist: "Ed Sheeran", music_df: music):
    """generates songs of favorite artist"""
    music_df = music_df[music_df.artists == artist]

    for _, row in music_df.iterrows():
        try: 
            yield row['name']
        except:
            StopIteration

#Closures
def get_music(music_df, measure):

    def get_high_energy_tracks(measure_level):
        """Submit your code and the tracks it finds, artist name, track name and energy value"""

        energy_tracks = music_df[music_df[measure] >= measure_level]

        for _, row in energy_tracks.iterrows():
            try:
                yield "Track: {track}, Artist: {artist}, Energy Level: {energy}".format(track = row['name'], artist = row['artists'], energy = row['energy'])
            except:
                StopIteration
                
    return get_high_energy_tracks





