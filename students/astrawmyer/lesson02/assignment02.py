import pandas as pd
music = pd.read_csv("featuresdf.csv")

def kendrick_generator():
    for x in music.artists:
        if x == 'Kendrick Lamar':
            yield x
            
kendrick = kendrick_generator()
for x in kendrick_generator():
    print(x)