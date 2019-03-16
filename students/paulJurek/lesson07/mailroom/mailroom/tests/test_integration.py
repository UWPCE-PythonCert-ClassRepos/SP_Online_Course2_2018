"""integration test suite for mailroom application.  This is focused on the 
donation controller integration with the data access layer.  The test
suite is setup so each test can be run for any of the databaes.  
To test additional databases, user should modify fixture to include setup for
additional database"""
import datetime
import pytest
from mailroom.DonationController import DonationController
from mailroom.SqliteDatabaseLayer import SQLiteAccessLayer

TEST_DATABASES = [SQLiteAccessLayer, SQLiteAccessLayer, SQLiteAccessLayer, SQLiteAccessLayer]

@pytest.fixture(scope="module",
                params=TEST_DATABASES)
def example_database(request):
    """each database will start wih blank database
    but with tables built"""
    print(type(request.param))
    print(request)
    db = request.param()
    db.db_init(':memory:')

    yield db
    
    db.close()

@pytest.fixture
def donation_controller(example_database):
    """sample controller for save the whales foundation
    setup with basic information 1 donor and 1 donation"""
    dc = DonationController(example_database)
    dc.create_donor(donor_name='test1', donor_email="test1")
    dc.create_donation(amount=500, donor='test1', date=datetime.datetime(2018,1,1))
    yield dc

#@pytest.mark.xfail(reason='not implemented')
def test_create_new_donor(donation_controller):
    """given a donation controller
    when user creates new donor
    the user is added to the donation controller"""
    donor = 'SantaClaus'
    while donation_controller.find_donor(donor):
            donor += 'a'
    assert donation_controller.find_donor(donor) is None
    donation_controller.create_donor(donor_name=donor)
    assert donation_controller.find_donor(donor).donor_name == donor