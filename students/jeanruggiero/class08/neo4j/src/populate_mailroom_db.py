"""
Populate mailroom.db with existing donor data.
"""

import pprint
import login_database


def populate_db(donor_list, db_name):

    with login_database.login_mongodb_cloud() as client:
        db = client[db_name]
        db.drop_collection('donors')
        db.drop_collection('donations')
        donors = db['donors']
        donations = db['donations']

        for donor, date_added, donation_list in donor_list:
            donors.insert_one({
                'name': donor,
                'date_added': date_added
                })
            for amount, date_donated in donation_list:
                donations.insert_one({
                    'amount': round(amount, 2),
                    'date': date_donated,
                    'donor': donor
                    })


if __name__ == '__main__':

    donors = [
        ('han solo', '2013-11-11', [(3468.34, '2013-11-14'), (457, '2014-11-05'), (34.2, '2018-01-02')]),
        ('luke skywalker', '2017-06-01', [(5286286.3, '2019-03-21'), (567, '2019-03-24'), (23.5678, '2017-07-06')]),
        ('chewbacca', '2011-01-01', [(432, '2011-09-06'), (679.4553, '2013-05-24')]),
        ('princess leia', '2008-12-29', [(5.3434, '2009-08-09')]),
        ('bobba fett, bounty hunter', '1954-07-05', [(67, '1954-07-05')])
    ]

    populate_db(donors, 'mailroom')
