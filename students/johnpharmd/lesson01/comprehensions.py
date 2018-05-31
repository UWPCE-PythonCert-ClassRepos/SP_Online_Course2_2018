import pandas as pd

# 1st exercise: Using Spotify 2017 top 100 track data and Pandas with List Comprehensions
music = pd.read_csv('featuresdf.csv')

print('music.head() returns:')
music.head()
print('music.describe() returns:')
music.describe()
