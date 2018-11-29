"""
Shin Tran
Python 220
Lesson 8 Assignment
Pickle Example
"""

import pickle
import pprint
import utilities

log = utilities.configure_logger('default', '../logs/mongodb_script.log')


def run_example():
    """
    Persistence and serialization scenarios
    """

    game_unit_data = [
        {'unit_name': 'Archer',
            'hit_points': 370,
            'damage': 126,
            'range': 5,
            'cost': 3},
        {'unit_name': 'Baby Dragon',
            'hit_points': 1544,
            'damage': 193,
            'range': 3.5,
            'cost': 4},
        {'unit_name': 'Barbarian',
            'hit_points': 927,
            'damage': 231,
            'range': 0,
            'cost': 5},
        {'unit_name': 'Golem',
            'hit_points': 6176,
            'damage': 376,
            'range': 0,
            'cost': 8},
        {'unit_name': 'Inferno Dragon',
            'hit_points': 1562,
            'damage': 511,
            'range': 3.5,
            'cost': 4},
        {'unit_name': 'Knight',
            'hit_points': 1968,
            'damage': 244,
            'range': 0,
            'cost': 3},
        {'unit_name': 'Magic Archer',
            'hit_points': 715,
            'damage': 140,
            'range': 7,
            'cost': 4},
        {'unit_name': 'Musketeer',
            'hit_points': 870,
            'damage': 256,
            'range': 6,
            'cost': 4},
        {'unit_name': 'Valkyrie',
            'hit_points': 2406,
            'damage': 322,
            'range': 0,
            'cost': 4},
        {'unit_name': 'Wizard',
            'hit_points': 870,
            'damage': 340,
            'range': 5.5,
            'cost': 5}
    ]

    """
    Write and read with pickle
    """
    log.info("\n\n====")
    log.info('Step 1: Demonstrate persistence with pickle')
    log.info('Write a pickle file with the game unit data')
    pickle.dump(game_unit_data, open('../data/data.pkl', 'wb'))

    log.info('Step 2: Now read it back from the pickle file')
    read_data = pickle.load(open('../data/data.pkl', 'rb'))
    
    log.info('Step 3: Show that the write and read were successful')
    assert read_data == game_unit_data
    log.info("and print the data")
    pprint.pprint(read_data)


if __name__ == '__main__':
    run_example()
