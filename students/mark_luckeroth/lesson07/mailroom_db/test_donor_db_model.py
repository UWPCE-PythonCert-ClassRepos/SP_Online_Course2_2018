"""
test code for donor_models.py

"""

import pytest
import math
from random import shuffle

from mailroom_db_model_2 import *
from cli_main import *
from donor_models import *


def test_donor_init():
    d1 = Donor_obj('Mark Luckeroth',1000.)
    assert d1.donor_name == 'Mark Luckeroth'
    assert d1.donations == [1000.]
    d2 = Donor_obj('Raja Koduri',[60., 60000.])
    assert d2.donor_name == 'Raja Koduri'
    assert d2.donations == [60., 60000.]


def test_list_donors():
    donor_list = list_donors()
    expected_donors = ['Peter Pan', 'Paul Hollywood', 'Mary Berry',
                    'Raja Koduri', 'Jake Turtle']
    for expected in expected_donors:
        assert expected in donor_list


def test_add_donor():
    assert 'Greg Luckeroth' not in list_donors()
    add_donor('Greg Luckeroth')
    assert 'Greg Luckeroth' in list_donors()


def test_add_donation():
    add_donation(1000., 'Greg Luckeroth')
    add_donation(2000., 'Greg Luckeroth')
    add_donation(3000., 'Greg Luckeroth')
    database = SqliteDatabase('mailroom.db')
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')
    query = (Donor
             .select(Donor.donor_name, Donation.amount)
             .join(Donation)
             .where(Donor.donor_name == 'Greg Luckeroth'))
    assert float(str(query[0].donation.amount)) == 1000.
    assert float(str(query[1].donation.amount)) == 2000.
    assert float(str(query[2].donation.amount)) == 3000.

    database.close()


