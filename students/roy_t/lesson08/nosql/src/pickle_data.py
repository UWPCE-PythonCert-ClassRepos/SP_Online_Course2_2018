"""
    Data for database demonstrations
"""
from numpy import random

def get_pickle_data():
    """
    demonstration data
    """
    header = ['Thermocouple_1', 'Thermocouple_2', 'Thermocouple_3',
                'Ambient_1', 'Ambient_2' , 'GPU_Tcase', 'VR_FET_1', 'VR_FET_2']
    typical = [53., 66., 83., 23., 22.7, 87.1, 95.3, 98.1]
    data = []
    data.append(header)
    for i in range(len(header)):
        temperatures = random.normal(typical[i], 1.5, 25)
        data.append(temperatures)
    return data
