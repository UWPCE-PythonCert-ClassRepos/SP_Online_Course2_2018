import pandas as pd
music = pd.read_csv('featuresdf.csv')

#determines the top 5 tracks based on danceability and loudness of song
def top_5():
    results = [(a, b, c, d) for a, b, c, d in zip(music.artists, music.name, music.danceability, music.loudness) if c > .7 and d < -4.0]
    results.sort(key=sort_by_danceability, reverse=True)
    top_5 = results[0:5]
    chart = '-' * 75
    for x in top_5:
        chart += f'\n{x[0]:<17} {x[1]:<36} ({x[2]:.4f}), ({x[3]:.4f})'
    chart += f'\n'
    chart += '-' * 75
    print(chart)

#function for sorting the tuples by 3rd element (danceability)
def sort_by_danceability(i):
    return i[2]

#runs the top_5 function if executable file is run
if __name__ == '__main__':
    top_5()