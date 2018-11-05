import pandas as pd
music = pd.read_csv("featuresdf.csv")

def artists_gen():
    ''' Write a generator to find and print all of your favorite artist’s tracks. 
    As it turns out The Weeknd has two tracks in this list: Starboy and I Feel It Comming. '''
    index = 0
    while index < len(music.artists):
        if music.artists[index] == "The Weeknd":
            yield (music.name[index])
        index += 1

def energy_closure():
    songs = [x for x in zip(music.energy, music.artists, music.name) if x[0] > 0.8]
    #sorted_songs = songs.sorted(reverse=True)
    def print_energy_tracks():
        for x in songs:
            print(f"{x[0]:4.2}\t{x[1]:16}\t{x[2]:35}")

    print_energy_tracks()



results = artists_gen()
results_sorted = sorted(results, reverse=True)
print("Tracks by The Weeknd are as follows: ")
for i in results_sorted:
    print(i)

energy_closure()
