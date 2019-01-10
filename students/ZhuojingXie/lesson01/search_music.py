import pandas as pd
music = pd.read_csv('featuresdf.csv')

data = [raw_data for raw_data in zip(music.artists, music.name, music.danceability, music.loudness)
        if (raw_data[2] > 0.8 and raw_data[3] < -0.5)]
data = sorted(data, key=lambda x: x[2], reverse=True)

for print_data in data[0:5]:
    print(print_data[0:2])
