# Author: Andy Kwok
# Last Updated: 10/29/18

#!/usr/bin/env python3


import pandas as pd

def find_high_energy(value):
    def read_file(name):
        data_csv = pd.read_csv(name)
        database = list(zip(data_csv.id, data_csv.name,
                            data_csv.artists,
                            data_csv.danceability,
                            data_csv.loudness, 
                            data_csv.energy))
        for item in database:
            if item[5] >= value:
                yield item
    return read_file

fildb = find_high_energy(0.8)("featuresdf.csv")

print('id' + ' '*25 + 'Name' + ' '*43 + 'Artists' + ' '*15 +
      'Danceability' + ' '*10 + 'Loudness' + ' '*5 + 'Energy')
print('='*150)

for i, j, k, l, m, n in fildb:
    print('{:25}  {:45}  {:20}  {:<20f}  {:<10f} {:>10f}'.format(i, j, k, l, m, n))