"""
Populate mailroom.db with existing donor data.
"""

from mailroom_model import *


def populate_db(database_name, donors):

    database = SqliteDatabase(database_name, pragmas={'foreign_keys': 1})
    for donor in donors:
        try:
            database.connect()
            with database.transaction():
                new_donor = Donor.create(name=donor[0], date_added=donor[1])
                new_donor.save()

                for donation in donor[2]:
                    new_donation = Donation.create(
                        amount=donation[0],
                        date=donation[1],
                        donor=donor[0]
                        )
                    new_donation.save()

        except Exception as e:
            raise e
        finally:
            database.close()


if __name__ == '__main__':

    donors = [
        ('han solo', '2013-11-11', [(3468.34, '2013-11-14'), (457, '2014-11-05'), (34.2, '2018-01-02')]),
        ('luke skywalker', '2017-06-01', [(5286286.3, '2019-03-21'), (567, '2019-03-24'), (23.5678, '2017-07-06')]),
        ('chewbacca', '2011-01-01', [(432, '2011-09-06'), (679.4553, '2013-05-24')]),
        ('princess leia', '2008-12-29', [(5.3434, '2009-08-09')]),
        ('bobba fett, bounty hunter', '1954-07-05', [(67, '1954-07-05')])
    ]

    database.init('mailroom.db')
    database.connect()
    database.create_tables([Donor, Donation])
    database.close()

    populate_db('mailroom.db', donors)
