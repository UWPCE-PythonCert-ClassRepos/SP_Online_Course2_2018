"""
    pickle assignment - MLB AL teams selected data
"""

from pathlib import Path
import learn_data
import pickle
import pprint
import utilities

log = utilities.configure_logger('default',
                                 '../logs/pickle_mlb2018_al_standings.log')


def run_example():
    """
    Write and read with pickle
    """
    log.info("\n\n====")
    log.info('Write a pickle file with baseball data')

    baseball_data = learn_data.get_baseball_data()
    pickle_f = Path(__file__).parent.parent / 'data/data.pkl'
    pickle.dump(baseball_data, open(pickle_f, 'wb'))

    log.info('Now read the data back from the pickle file')
    read_data = pickle.load(open(pickle_f, 'rb'))
    log.info('Show that the write and read were successful')
    print('assert read_data == baseball_data')
    try:
        assert read_data == baseball_data
        log.info('True')
    except AssertionError:
        raise Exception
    log.info("and print the data")
    pprint.pprint(read_data)


if __name__ == '__main__':
    run_example()
