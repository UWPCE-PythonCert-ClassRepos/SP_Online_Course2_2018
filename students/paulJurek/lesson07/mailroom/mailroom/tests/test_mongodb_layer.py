"""tests the mongodb database layers work to spec"""
import datetime
import pytest

import mailroom.MongoDBDatabaseLayer as mdb
import mailroom.SqliteDatabaseLayer as sdb

def setup_mongo():
    db = mdb.MongoDBAccessLayer()
    # test used to ensure we don't overwrite actual database
    db.db_init(run_mode='test')
    # drops databae to start work from clean enviroment
    mdb.Donor.drop_collection()
    # fill in database with updated collections
    d1 = mdb.Donor(donor_name='test1',
               email='test1@gmail.com',
               donations=[mdb.Donation(100, datetime.datetime(2018,1,1)),
                          mdb.Donation(200, datetime.datetime(2019,1,1))]
              )
    d1.save()
    d2 = mdb.Donor(donor_name='test2',
               email='test2@gmail.com',
               donations=[mdb.Donation(100, datetime.datetime(2018,1,1)),
                          mdb.Donation(200, datetime.datetime(2019,1,1))]
              )
    d2.save()

    return db

def setup_sqlite():
    db = sdb.SQLiteAccessLayer()
    # test used to ensure we don't overwrite actual database
    db.db_init(':memory:')
    # drops databae to start work from clean enviroment

    # fill in database with updated collections
    sdb.Donor.create(donor_name='test1',
                     email='test1@gmail.com')
    sdb.Donation.create(donation_donor='test1',
                        donation_amount=100,
                        donation_date=datetime.datetime(2018,1,1))
    sdb.Donation.create(donation_donor='test1',
                        donation_amount=200,
                        donation_date=datetime.datetime(2019,1,1))
    
        # fill in database with updated collections
    sdb.Donor.create(donor_name='test2',
                     email='test2@gmail.com')
    sdb.Donation.create(donation_donor='test2',
                        donation_amount=100,
                        donation_date=datetime.datetime(2018,1,1))
    sdb.Donation.create(donation_donor='test2',
                        donation_amount=200,
                        donation_date=datetime.datetime(2019,1,1))

    return db


databases_to_test = (setup_mongo, setup_sqlite)

@pytest.fixture(params=databases_to_test)
def testing_database(request):
    """sets up database and fills with donors and donations"""
    db = request.param()

    yield db



def test_summarize_donors(testing_database):
    """given a database
    when summarize_donors is called on database
    a dict with donor summary is returned"""
    expected_result = {'test1': {'donor_name': 'test1',
                                 'donation_total': 300,
                                 'donation_count': 2,
                                 'average_donation': 150},
                       'test2': {'donor_name': 'test2',
                                 'donation_total': 300,
                                 'donation_count': 2,
                                 'average_donation': 150}
                        }
    assert testing_database.summarize_donors() == expected_result


def test_get_donations(testing_database):
    """given a donations database
    when get_donations is run for each donor
    a dic of the donations of the donor is returend"""
    donor = "test1"
    expected_output = {1: {'id': 1,
                   'donation_date': datetime.datetime(2018,1,1),
                   'donation_amount_cents': 100},
               2: {'id': 2,
                   'donation_date': datetime.datetime(2019,1,1),
                   'donation_amount_cents': 200}
               }
    assert testing_database.get_donations(donor) == expected_output


def test_create_donation(testing_database):
    """when donation is created
    true is returned if successful"""
    assert testing_database.create_donation(donor='test1', amount=23) is True

@pytest.mark.xfail(reason = 'need to figure out how to pass donor')
def test_find_donor(testing_database):
    """given a database
    when we search for donor
    the correct donor object is returned"""
    donor = testing_database.find_donor(donor_name='test1')
    assert isinstance(donor, Donor)
    assert donor.donor_name == 'test1'
    assert donor.email == 'test1@gmail.com'

@pytest.mark.xfail(reason = 'need to figure out how to pass donor')
def test_create_donor(testing_database):
    """given a database
    when we add a donor
    we can use find_donor method to get donor"""
    assert testing_database.find_donor(donor_name='test3') is None
    testing_database.create_donor(donor_name='test3')
    donor = testing_database.find_donor(donor_name='test3')
    assert isinstance(donor, Donor)


def test_get_total_donations(testing_database):
    """given a database
    when get_total_donations is called
    the donation total in database is returned"""
    assert testing_database.get_total_donations() == 600


def test_get_donors(testing_database):
    """given a database
    when get_donors is called
    a set of donor names is returned"""
    assert testing_database.get_donors() == set(['test1', 'test2'])


def test_update_donation(testing_database):
    """given a database
    when update_donation is called
    the total amount is updated"""
    assert testing_database.get_total_donations() == 600
    testing_database.update_donation(donor='test1', donation=1, value=1000)
    assert testing_database.get_total_donations() == 1500


def test_update_donor(testing_database):
    """given a database
    when update_donor is called
    the donor is now updated"""
    testing_database.update_donor(donor='test1',
                                  value='new_email@gmail.com')
    donor = testing_database.find_donor('test1')
    assert donor.email == 'new_email@gmail.com'


def test_delete_donation(testing_database):
    """given a database
    when delete_donation is called
    the total donation is modified"""
    testing_database.delete_donation(donation=0, donor='test1')
    assert testing_database.get_total_donations() == 500


def test_delete_donor(testing_database):
    """given a database
    when delete_donor is called
    the total donation is modified"""
    testing_database.delete_donor('test1')
    assert testing_database.get_total_donations() == 300


def test_get_donor_details(testing_database):
    """given a databae
    when get_donor_details is called
    the dict with results is returned minus donations"""
    expected_result = {'donor': 'test1',
                       'email': 'test1@gmail.com'}
    assert testing_database.get_donor_details(donor_name='test1') == expected_result


def test_get_donation_details(testing_database):
    """given a database
    when get_donation_details is called
    details of donatoin are returned in dict"""
    expected_result = {'donation': 0,
                       'donation_amount_cents': 100,
                       'donation_date': datetime.datetime(2018,1,1)}
