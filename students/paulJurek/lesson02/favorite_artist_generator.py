"""module to create a generator to get favorite artist from 
spotify top artist csv as part of Python 220 lesson 02.  
The favorite artist file can be downloaded from https://www.kaggle.com/nadintamer/top-tracks-of-2017
or the class website"""
import csv 

def get_artist_tracks(artist: str, filename: str) -> str:
    """generator which iterates through the specified file and 
    returns tracks for artist.  Using a generator to iteratre through file 
    to enable very large file handling
    args:
        artist: indifies the artist we are searching for
        filename: filename to search in
    returns:
        returns tracks for artist in file"""
    artist_name = 2
    track_name = 1
    print(filename)
    with open(filename, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[artist_name] == artist:
                print(row[track_name])
                yield row[track_name]

if __name__ == '__main__':
    print(set(get_artist_tracks(artist='Ed Sheeran', 
                          filename=r'top-tracks-of-2017.csv')))