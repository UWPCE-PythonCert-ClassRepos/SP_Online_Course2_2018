"""
Bring up an interpreter and load the data. (Data set link - right-click and download top-tracks-of-2017.zip)

import pandas as pd
music = pd.read_csv("featuresdf.csv")

Take a look around to get a sense of the general shape of the data.

music.head()
music.describe()

Now we are ready for the analytics. This first one is a gimme. We will use a comprehension to get danceability scores over 0.8.

[x for x in music.danceability if x > 0.8]

Your job, now, is to get artists and song names for for tracks with danceability scores over 0.8 and loudness scores below -5.0. In other words, quiet yet danceable tracks. Also, these tracks should be sorted in descending order by danceability so that the most danceable tracks are up top. You should be able to work your way there starting with the comprehension above. And while you could use Pandas features along the way, you don’t need to. To accomplish the objective you do not need to know anything more about Pandas than what you can infer from the material herein. Standard library functions that could come in handy include zip() and sorted().
"""

import pandas as pd

pd.options.display.max_columns = 999

# load data 
# The data file was downloaded directly from the KAGGLE website
# https://www.kaggle.com/nadintamer/top-tracks-of-2017 as I was getting errors
# with referenced link.  
DATA_FILE = "top-tracks-of-2017.csv"
df = pd.read_csv(DATA_FILE)

def limit_records_pandas(df):
    """this uses some of pandas methods to get to correct 
    results and sorts"""
    return df[(df['danceability']>0.8) & (df['loudness']<-5.0)].sort_values('danceability', ascending=False)

def limit_records_listcomps(df):
    """using iterrows still"""
    return [(row['name'], row['artists']) for _, row in df.sort_values('danceability', ascending=False).iterrows() if (row['danceability']>0.8) & (row['loudness']<-5) ]

def limit_records_zip(df):
    """filters dataframe using zip"""
    return sorted([(x[0], x[1]) for x in zip(df.name, df.artists, df.danceability, df.loudness) 
                    if (x[2]>0.8) & (x[3]<-5.0)])

if __name__=='__main__':
    print(limit_records_pandas(df).head(5))
    print(limit_records_listcomps(df)[:5])
    print(limit_records_zip(df)[:5])