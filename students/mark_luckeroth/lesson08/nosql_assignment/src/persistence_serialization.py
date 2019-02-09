"""
pickle data demonstration
"""

import pickle

import pprint
import utilities

log = utilities.configure_logger('default', '../logs/mongodb_script.log')

import collections
compare = lambda x, y: collections.Counter(x) == collections.Counter(y)

def pickle_data(data):
    """
    Write and read with pickle
    """
    log.info("\n\n====")
    log.info('Step 1: Demonstrate persistence with pickle')

    pickle.dump(data, open('../data/pickle_test.pkl', 'wb'))

    log.info('Step 2: Now read it back from the pickle file')
    read_data = pickle.load(open('../data/pickle_test.pkl', 'rb'))
    log.info('Step 3: Show that the write and read were successful')
    for orig, read in zip(data, read_data):
        if compare(orig, read):
            continue
        else:
            print('THE DATA DO NOT MATCH!')
            break
    log.info("and print the data")
    pprint.pprint(read_data)