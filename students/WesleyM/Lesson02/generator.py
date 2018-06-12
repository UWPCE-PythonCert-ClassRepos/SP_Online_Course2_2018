import pandas as pd
music = pd.read_csv("featuresdf.csv")

result = sorted([x for x in
                 zip(music.artists, music.name) if x[0] == 'Ed Sheeran'])
for i in result:
    print(i[0] +' - '+ i[1])
    
