import pandas as pd
music = pd.read_csv("featuresdf.csv")

def both_gen():
    ''' for any row, if danceability and loudness pass their tests
    yield the danceability, artist, and song of that row'''
    count = 0
    while count < len(music.danceability):
        if music.danceability[count] > 0.8 and music.loudness[count] < -5.0:
            yield (music.danceability[count], music.artists[count], music.name[count])
        count += 1

results = both_gen()
results_sorted = sorted(results, reverse=True) # sorts by danceability as that is yielded first
for i in results_sorted:
    print(i)
'''
Top songs returned:
(0.927, 'Migos', 'Bad and Boujee (feat. Lil Uzi Vert)')
(0.927, 'Drake', 'Fake Love')
(0.904, 'Kendrick Lamar', 'HUMBLE.')
(0.884, '21 Savage', 'Bank Account')
(0.8759999999999999, 'Jax Jones', "You Don't Know Me - Radio Edit")
'''