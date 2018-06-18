%cd C:/Users/kuhnb/pythoncourse2/SP_Online_Course2_2018/students/kuhnbt/lesson1

import pandas as pd

df = pd.read_csv('featuresdf.csv')
music_subset = zip(df.name, df.artists, df.danceability, df.loudness)

quiet_danceable = sorted([i for i in music_subset if i[2]>.8 and i[3]<-5.0],
                         key=lambda x: x[2], reverse=True)

quiet_danceable = [i[:2] for i in quiet_danceable][:5]

print(quiet_danceable)