try:
    import sys
    import pandas as pd
except ModuleNotFoundError:
    print("Must use Python 2 for pandas module")
    sys.exit()


def high_energy_tracks(high=0.8):
    m = pd.read_csv("featuresdf.csv")
    def tracks():
        return ((t, a, e) for t, a, e in zip(m.name, m.artists, m.energy)
                if e > high)
    return tracks


if __name__ == "__main__":
    x = high_energy_tracks()
    with open('high_energy_closure.txt', 'w+') as hec:
        for y in x():
            print(y)
            hec.write(str(y))
