import pandas as pd
music = pd.read_csv("featuresdf.csv")

result = sorted([x for x in
                 zip(music.artists, music.name) if x[0] == 'Ed Sheeran'])

def track_generator(music_data):
    for i in music_data:
        yield i

ed_sheeran = track_generator(result)
print(next(ed_sheeran))
    
