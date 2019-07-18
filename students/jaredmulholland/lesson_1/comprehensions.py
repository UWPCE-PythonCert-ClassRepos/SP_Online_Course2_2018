import pandas as pd 

music = pd.read_csv("C:\\Users\\Jared\\Documents\\Python220\\SP_Online_Course2_2018\\students\\jaredmulholland\\lesson_1\\featuresdf.csv")

"""
Your job, now, is to get artists and song names for for tracks with danceability scores over 0.8 and loudness scores below -5.0. 
In other words, quiet yet danceable tracks. Also, these tracks should be sorted in descending order by danceability so that the most danceable tracks are up top. 
You should be able to work your way there starting with the comprehension above. And while you could use Pandas features along the way, you don’t need to. 
To accomplish the objective you do not need to know anything more about Pandas than what you can infer from the material herein. 
Standard library functions that could come in handy include zip() and sorted().

Submit your code and the top five tracks to complete the assignment.

Then, put on your dancing shoes, get out to Spotify or Youtube, and let’s get this party started. Stay safe. It’s a scary pop world out there.
"""

songs = [x for x in zip(music.name, music.artists, music.danceability, music.loudness) if x[2] > 0.8 and x[3] < -5.0]

def danceability_sort(x):
    return x[2]

for song in sorted(songs, key=danceability_sort, reverse=True)[0:5]:
    print(song)