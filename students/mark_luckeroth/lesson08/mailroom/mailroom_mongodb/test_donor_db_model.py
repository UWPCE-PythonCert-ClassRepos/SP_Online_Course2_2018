"""
test code for donor_models.py

"""

import pytest
import math
from random import shuffle
import login_database


from cli_main import *
from donor_models import *
from build_mailroom_db_2 import *

def test_db_build():
    populate_donordata()
    assert True


def test_donor_init():
    d1 = Donor_obj('Mark Luckeroth',1000.)
    assert d1.donor_name == 'Mark Luckeroth'
    assert d1.donations == [1000.]
    d2 = Donor_obj('Raja Koduri',[60., 60000.])
    assert d2.donor_name == 'Raja Koduri'
    assert d2.donations == [60., 60000.]


# def test_list_donors():
#     with login_database.login_mongodb_cloud() as client:
#         donors = client['mailroom']['donors']
#         donor_list = list_donors()
#     expected_donors = ['Peter Pan', 'Paul Hollywood', 'Mary Berry',
#                     'Raja Koduri', 'Jake Turtle']
#     for expected in expected_donors:
#         assert expected in donor_list


# def test_add_donor():
#     with login_database.login_mongodb_cloud() as client:
#         donors = client['mailroom']['donors']
#         assert 'Greg Luckeroth' not in list_donors()
#         add_donor('Greg Luckeroth')
#         assert 'Greg Luckeroth' in list_donors()


# def test_add_donation():
#     with login_database.login_mongodb_cloud() as client:
#         donors = client['mailroom']['donors']
#         add_donation(1000., 'Greg Luckeroth')
#         add_donation(2000., 'Greg Luckeroth')
#         add_donation(3000., 'Greg Luckeroth')
#         query = {'name': 'Greg Luckeroth'}
#         results = donors.find_one(query)

#         assert results[amount] == [1000., 2000., 3000.]



