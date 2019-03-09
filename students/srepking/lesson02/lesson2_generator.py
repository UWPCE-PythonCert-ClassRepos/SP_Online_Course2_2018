import pandas as pd
music = pd.read_csv("featuresdf.csv")



def find_favorite(name):
        for artist, song in zip(music.artists, music.name):
            if artist == str(name):
                yield (artist, song)

if __name__ == '__main__':
    print('\n\nUsing a Generator to find your favorite Artist')
    favorites = find_favorite('Ed Sheeran')
    for x in favorites:
        print(x)





