#!/usr/bin/env python3
"""Lesson02 Closures Module"""

import pandas as pd


def high_energy_closure(df, energy_level=0.8):
    """Closure for generating functions that print artists and tracks that are
       have an energy level above the specified value.

    Args:
        df (dataframe): Pandas dataframe
        energy_level (float, optional): Defaults to 0.8. Energy Level

    Returns:
        func: Function that prints results
    """
    data = (x for x in sorted(zip(df.artists, df.name, df.energy),
                              key=lambda y: y[2], reverse=True)
            if x[2] > energy_level)

    def print_data():
        """Print high energy results based on data set"""

        print(f'HIGH ENERGY LEVEL: {energy_level:.2f}')
        for d in data:
            print(f'{d[0]:<40}{d[1]:<60}{d[2]:<40.3f}')

    return print_data


music = pd.read_csv("featuresdf.csv")
high_energy_08 = high_energy_closure(music)
high_energy_09 = high_energy_closure(music, 0.9)
high_energy_07 = high_energy_closure(music, 0.7)

high_energy_08()
print()
print()
high_energy_09()
print()
print()
high_energy_07()
