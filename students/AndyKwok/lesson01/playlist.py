# Author: Andy Kwok
# Last Updated: 10/23/18

#!/usr/bin/env python3

import pandas as pd
music = pd.read_csv("featuresdf.csv")

newdb = list(zip(music.id, music.name, music.artists,
                 music.danceability, music.loudness))

fildb = [i for i in newdb if i[3] > 0.8 and i[4] < -5.0]

sfildb = sorted(fildb, key=lambda title: title[3], reverse=True)

print('id' + ' '*25 + 'Name' + ' '*38 + 'Artists' + ' '*10 +
      'Danceability' + ' '*10 + 'Loudness')
print('='*120)

for i, j, k, l, m in sfildb[:5]:
    print('{:25}  {:40}  {:15}  {:<20}  {:<10}'.format(i, j, k, l, m))
