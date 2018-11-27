#!/usr/bin/env python3

import logging
from create_donor import *
from mailroom import Donor, Donations

PERSON_NAME = 0
DONATION_LIST = 1

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
database = SqliteDatabase('donation.db')

Donors = [
        ('John', [2000.0]),
        ('Mason', [1000.0, 200.0, 3500.0]),
        ('Amy', [90000.0]),
        ('Allen', [9000.0, 600000.0, 9000.0, 700]),
        ('Jill', [99000.0])
        ]

collection = Donations()


def test_add():
    """test adding donor to database"""

    Donor_Collection.delete().execute()
    Donation_Amount.delete().execute()

    for item in Donors:
        donor = Donor(item[PERSON_NAME], item[DONATION_LIST])
        collection.add_update(donor)

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        for donor in Donors:
            db_donor = Donor_Collection.get(Donor_Collection.person_name == donor[PERSON_NAME])
            assert(db_donor.person_name == donor[PERSON_NAME])
            assert(db_donor.donation_count == len(donor[DONATION_LIST]))
            assert(db_donor.total_amount == sum(donor[DONATION_LIST]))

            db_amounts = Donation_Amount.select().where(Donation_Amount.from_person == donor[PERSON_NAME])
            assert(len(db_amounts) == len(donor[DONATION_LIST]))
            for amount in db_amounts:
                assert(amount.donation_amount in donor[DONATION_LIST])

    except Exception as e:
        assert(False)
    finally:
        database.close()

def test_update():
    """ test updating a donor in database"""

    Donor_Collection.delete().execute()
    Donation_Amount.delete().execute()

    # add a donor to db
    donor = Donor('Willam Gates',[50000.0])
    collection.add_update(donor)

    # update door
    donor = Donor('Willam Gates',[40000.0])
    collection.add_update(donor)
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        db_donor = Donor_Collection.get(Donor_Collection.person_name == donor._name)
        assert(db_donor.person_name == donor._name)
        assert(db_donor.donation_count == 2)
        assert(db_donor.total_amount == 90000.0)

        db_amounts = Donation_Amount.select().where(Donation_Amount.from_person == donor._name)
        assert(len(db_amounts) == 2)

        sum = 0
        for amount in db_amounts:
            sum +=amount.donation_amount
        assert(sum == 90000.0 )

    except Exception as e:
        assert(False)

    finally:
        database.close()

def test_delete():
    """ test deleting a donor from database"""

    Donor_Collection.delete().execute()
    Donation_Amount.delete().execute()

    for item in Donors:
        donor = Donor(item[PERSON_NAME], item[DONATION_LIST])
        collection.add_update(donor)

    # delete donor John
    collection.delete('John')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        donor = Donor_Collection.select().where( Donor_Collection.person_name == 'John')
        assert(False)

    except Exception as e:
        pass
    finally:
        database.close()