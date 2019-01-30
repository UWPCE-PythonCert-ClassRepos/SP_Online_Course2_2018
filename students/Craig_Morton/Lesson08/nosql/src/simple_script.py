# ------------------------------------------------- #
# Title: Lesson 8, Pickling
# Dev:   Craig Morton
# Date:  1/15/2019
# Change Log: CraigM, 1/15/2018, Pickling
# ------------------------------------------------- #

import pickle
import pprint
import utilities

log = utilities.configure_logger('default', '../logs/mongodb_script.log')


def pickle_example():
    """
    Persistence and serialization scenarios
    """

    car_data = [
        {'manufacturer': 'F1',
         'model': 'McLaren',
         'mpg': 15,
         'weight': 2420,
         'horsepower': 659},
        {'manufacturer': 'Bugatti',
         'model': 'Chiron',
         'mpg': 19,
         'weight': 2782,
         'horsepower': 466},
        {'manufacturer': 'Mercedes',
         'model': 'Project ONE',
         'mpg': 12,
         'weight': 3102,
         'horsepower': 573},
        {'manufacturer': 'McLaren',
         'model': 'Senna',
         'mpg': 17,
         'weight': 2989,
         'horsepower': 800},
        {'manufacturer': 'Koenigsegg',
         'model': "Agera RS",
         'mpg': 18,
         'weight': 2544,
         'horsepower': 348},
        {'manufacturer': 'Pagani',
         'model': "Zonda",
         'mpg': 14,
         'weight': 2659,
         'horsepower': 698},
        {'manufacturer': 'Porsche',
         'model': 'RS3',
         'mpg': 15,
         'weight': 3122,
         'horsepower': 458},
        {'manufacturer': 'Ferrari',
         'model': '458',
         'mpg': 22,
         'weight': 3216,
         'horsepower': 587},
        {'manufacturer': 'Aston Martin',
         'model': "Vantage",
         'mpg': 25,
         'weight': 2733,
         'horsepower': 761},
        {'manufacturer': 'Lamborghini',
         'model': "Aventador",
         'mpg': 21,
         'weight': 3309,
         'horsepower': 490}
    ]

    """
    Write and read with pickle
    """
    log.info("\n\n====")
    log.info('Step 1: Demonstrate persistence with pickle')
    log.info('Step 2: Write car data to pickle file')
    pickle.dump(car_data, open('../data/data.pkl', 'wb'))

    log.info('Step 3: Read from pickle file')
    read_data = pickle.load(open('../data/data.pkl', 'rb'))

    log.info('Step 4: Confirm write and read')
    assert read_data == car_data
    log.info("Step 5: Data presentation")
    pprint.pprint(read_data)


if __name__ == '__main__':
    pickle_example()
