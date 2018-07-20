"""
Data to populate mailroom db
"""


import login_database
import utilities
import os
import db_ops


try:
    os.chdir('../logs')
except OSError:
    os.mkdirs('../logs')


log = utilities.configure_logger('default', '../logs/mailroom_mongodb.log')


def get_donors_data():
    """
    current donors
    :return:
    """
    donations = [
        {
            'donor_name': 'Jerry Seinfeld',
            'donations': [
                100.0,
                200.0,
                199.1
            ]

        },
        {
            'donor_name': 'George Costanza',
            'donations': [
                22.0,
                300.0,
                24.1
            ]

        },
        {
            'donor_name': 'Elaine Bennis',
            'donations': [
                11.0,
                2.1,
                66.1
            ]

        },
        {
            'donor_name': 'Cosmo Kramer',
            'donations': [
                0.1,
                0.22,
                0.3
            ]

        },
        {
            'donor_name': 'Newman',
            'donations': [
                20.0,
                11.0,
                5.13
            ]

        }
    ]
    return donations


def start_db():
    """
    connect to mongodb and populate the data
    :return:
    """
    with login_database.login_mongodb_cloud() as client:
        log.info('Step 1: We are going to use a database called dev')
        log.info('But if it doesnt exist mongodb creates it')
        db = client['dev']

        log.info('And in that database use a collection called mailrrom')
        log.info('If it doesnt exist mongodb creates it')

        mailroom = db['mailroom']

        log.info('Step 2: Now we add donors data')
        donors = get_donors_data()
        mailroom.insert_many(donors)
    log.info('DB was successfully initialized')


if __name__ == '__main__':
    start_db()
    # db_ops.update_donations('Jerry Seinfeld', 500)
    # db_ops.list_donors()
    # db_ops.get_total_for_donor('Jerry Seinfeld')