# Nebiat Abraha 
# Comprehensions


import pandas as pd
import itertools
music = pd.read_csv("featuresdf.csv")

dance = music['name'][music['danceability'] > .8][music['loudness'] < -5]
dance.head(5)

# Top 5 songs: 
# HUMBLE.
# Mask off
# Passionfruit
# Strip that Down
# Bad and Boujee

# Iterators & Iterables
class IterateMe_2:
    """
    About as simple an iterator as you can get:

    returns the sequence of numbers from zero to 10
    ( like range(10) ) with default step of 1
    """

    def __init__(self, current=-1, stop=10, step=1):
        self.current = current
        self.stop = stop
        self.step = step

    def __iter__(self):
        return self
    
    def __next__(self):
        self.current += self.step
        if self.current < self.stop:
            return self.current
        else:
            raise StopIteration


# Generators

def doubler():
    for n in itertools.count():
        yield 2**n  

def intsum():
    for n in itertools.accumulate(itertools.count()):
        yield n

def fib():
    x = 0
    y = 1
    while True:
        yield x
        x, y = y, x + y

def prime():
    for x in itertools.count(2):
        # number is considered prime, until proven otherwise
        prime = True
        # checks modulus of all numbers under x, except 1
        for n in range(2, x):
            if x%n == 0:
                prime = False
        if prime:
            yield x