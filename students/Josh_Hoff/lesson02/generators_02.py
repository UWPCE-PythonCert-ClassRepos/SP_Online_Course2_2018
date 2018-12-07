import pandas as pd
music = pd.read_csv('featuresdf.csv')

def favorites():
    results = [(a, b) for a, b in zip(music.artists, music.name) if a == 'The Chainsmokers']
    for x in results:
        yield x[1]

if __name__ == "__main__":
    favorites()
    print('Songs by "The Chainsmokers" have been loaded.')
    
"""What this generates:
'Something Just Like This'
'Paris'
'Closer'
'Don't Let Me Down'"""