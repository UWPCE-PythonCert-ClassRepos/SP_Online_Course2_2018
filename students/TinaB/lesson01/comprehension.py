#!/usr/bin/env python3

"""
import pandas as pd
music = pd.read_csv("featuresdf.csv")
Take a look around to get a sense of the general shape of the data.

music.head()
music.describe()
Now we are ready for the analytics. This first one is a gimme. We will use a comprehension to get danceability scores over 0.8.

[x for x in music.danceability if x > 0.8]
Your job, now, is to get artists and song names for for tracks with danceability scores over 0.8 and loudness scores below -5.0. In other words, quiet yet danceable tracks. Also, these tracks should be sorted in descending order by danceability so that the most danceable tracks are up top. You should be able to work your way there starting with the comprehension above. And while you could use Pandas features along the way, you don’t need to. To accomplish the objective you do not need to know anything more about Pandas than what you can infer from the material herein. Standard library functions that could come in handy include zip() and sorted().

Submit your code and the top five tracks to complete the assignment.

Then, put on your dancing shoes, get out to Spotify or Youtube, and let’s get this party started. Stay safe. It’s a scary pop world out there.
"""

import pandas as pd
music = pd.read_csv("featuresdf.csv")

#gets all songs from list matching selection criteria
sorted([x for x in zip(music.artists, music.name, music.danceability, music.loudness) 
 if x[2] > 0.8 and x[3] < -5.0], key = lambda x : x[2], reverse = True)

#gets top five tracks
top5 = sorted([x for x in zip(music.artists, music.name, music.danceability, music.loudness) 
 if x[2] > 0.8 and x[3] < -5.0], key = lambda x : x[2], reverse = True)[:5]

#clean up for output
for x in top5:
    print('{:20} \t{:35} \t{:f} \t{:f}'.format(x[0],x[1],x[2],x[3]))
