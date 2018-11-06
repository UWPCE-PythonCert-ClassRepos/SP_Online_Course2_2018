# Author: Andy Kwok
# Last Updated: 10/29/18

#!/usr/bin/env python3

import pandas as pd
music = pd.read_csv("featuresdf.csv")

db = list(zip(music.id, music.name, music.artists,
                 music.danceability, music.loudness))
		 
def find_artist(database, artist):
	for	item in database:
		if item[2] == artist:
			yield item

fildb = find_artist(db, "Ed Sheeran")
			
print('id' + ' '*25 + 'Name' + ' '*38 + 'Artists' + ' '*10 +
      'Danceability' + ' '*10 + 'Loudness')
print('='*120)

for i, j, k, l, m in fildb:
    print('{:25}  {:40}  {:15}  {:<20}  {:<10}'.format(i, j, k, l, m))