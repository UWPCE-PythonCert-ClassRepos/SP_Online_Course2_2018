"""
Data to populate mailroom db
"""


import login_database
import utilities
import os
import db_ops
import json


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
    donors = [
        {"donor_name": "Jerry Seinfeld", 'donations': [100.0, 200.0, 199.1]},
        {"donor_name": "George Constanza", 'donations': [22.0, 300.0, 24.1]},
        {"donor_name": "Elaine Bennis", 'donations': [11.0, 2.1, 66.1]},
        {"donor_name": "Cosmo Kramer", 'donations': [0.11, 0.21, 0.3]},
        {"donor_name": "Newman", 'donations': [20.0, 11.0, 5.13]}
    ]
    donors_json = json.dumps(donors)
    log.info('JSON of donors: {}'.format(donors_json))
    r = login_database.login_redis_cloud()
    # setting users and emails
    r.set('donors', donors_json)


def start_db():
    """
    connect to mongodb and populate the data
    :return:
    """
    get_donors_data()


if __name__ == '__main__':
    # start_db()
    # db_ops.update_donations('Jerry Seinfeld', 500)
    # db_ops.list_donors()
    db_ops.get_total_for_donor('Jerry Seinfeld')