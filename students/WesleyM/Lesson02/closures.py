import pandas as pd

def get_artist(music, energy_level=0.8):
        result = sorted([x for x in
          zip(music.artists, music.name, music.energy)
          if x[2] >= energy_level], key = lambda x:x[2], reverse=True)
        def high_energy():
            print('{:20}\t{:40}\t{:5}'.format('Artist', 'Title', 'Energy Level'))
            for x in result:
                print('{:20}\t{:40}\t{:5.3f}'.format(x[0], x[1], x[2]))
        return high_energy

music = pd.read_csv("featuresdf.csv")
playlist = get_artist(music, 0.5)
playlist()


    
