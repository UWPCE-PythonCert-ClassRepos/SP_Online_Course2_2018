import pandas as pd
music = pd.read_csv("featuresdf.csv")

#Using the Comprehension to Find Ed Sheeren's Tracks
qualified = [(artist, song, danceability, loudness)
                  for artist, song, danceability, loudness
                  in zip(music.artists,music.name,music.danceability,music.loudness)
                  if (str(artist) == 'Ed Sheeran')]
qualified_sorted=sorted(qualified,key= lambda sort_by: sort_by[2], reverse=True)
print(qualified_sorted)

#Using a Generator to find Ed Sheeren's Tracks

def find_favorite(name):
        for artist, song in zip(music.artists, music.name):
            if artist == str(name):
                yield (artist, song)

if __name__ == '__main__':
    print('\n\nUsing a Generator to find your favorite Artist')
    favorites = find_favorite('Ed Sheeran')
    for x in favorites:
        print(x)





