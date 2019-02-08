#-------------------------------------------------#
# Title: Generators
# Dev:   LDenney
# Date:  February 6th, 2019
# ChangeLog: (Who, When, What)
#   Laura Denney, 2/6/19, Started work on generators assignment
#-------------------------------------------------#

##IMAGINE DRAGONS

'''id', 'name', 'artists', 'danceability', 'energy', 'key',
       'loudness', 'mode', 'speechiness', 'acousticness',
       'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms',
       'time_signature'
'''

import pandas as pd
music = pd.read_csv("featuresdf.csv")

def imagine_dragons():
    count = 0
    while count <len(music):
        if music.loc[count,"artists"] == "Imagine Dragons":
            yield music.loc[count,"name"]
        count +=1

dragon_generator = imagine_dragons()
print("Imagine Dragon songs: ",[x for x in dragon_generator])

###################################################

