import csv

def get_high_energy_tracks(energy_level_limit):

    
    def get_tracks_by_energy_level(filename: str=r'lesson02\top-tracks-of-2017.csv'):
        """general function which searches and returns specific energy level records"""
        artist_name = 2
        track_name = 1
        energy_level = 4
        with open(filename, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                try:
                    if float(row[energy_level]) >= energy_level_limit:
                        yield (row[track_name], row[artist_name], row[energy_level])
                except ValueError:
                    # catches first line an skips
                    continue
    return get_tracks_by_energy_level

if __name__ == '__main__':
    t = get_high_energy_tracks(energy_level_limit=0.8)
    test = t()
    print(set(test))
