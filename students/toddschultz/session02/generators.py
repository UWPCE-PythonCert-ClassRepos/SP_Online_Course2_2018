import pandas as pd
music = pd.read_csv("featuresdf.csv")

def artists_gen():
    ''' Write a generator to find and print all of your favorite artist’s tracks. '''
    index = 0
    while index < len(music.artists):
        if music.artists[index] == "The Weeknd":
            yield (music.name[index])
        index += 1

results = artists_gen()
results_sorted = sorted(results, reverse=True)
print("Tracks by The Weeknd are as follows: ")
for i in results_sorted:
    print(i)



'''
As it turns out The Weeknd has two tracks in this list: Starboy and I Feel It Comming. 
'''