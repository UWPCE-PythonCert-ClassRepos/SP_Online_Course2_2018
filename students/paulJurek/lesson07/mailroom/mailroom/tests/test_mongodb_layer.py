"""tests the mongodb database layers work to spec"""
import datetime
import pytest 

from mailroom.MongoDBDatabaseLayer import MongoDBAccessLayer, Donor, Donation

@pytest.fixture
def testing_database():
    """sets up database and fills with donors and donations"""
    db = MongoDBAccessLayer()
    # test used to ensure we don't overwrite actual database
    db.db_init(run_mode='test')
    # drops databae to start work from clean enviroment
    Donor.drop_collection()

    # fill in database with updated collections
    d1 = Donor(donor_name='test1',
               email='test@gmail.com',
               donations=[Donation(100, datetime.datetime(2018,1,1)),
                         Donation(200, datetime.datetime(2019,1,1))]
                         )
    d1.save()
    d2 = Donor(donor_name='test2',
               email='test2@gmail.com',
               donations=[Donation(100, datetime.datetime(2018,1,1)),
                         Donation(200, datetime.datetime(2019,1,1))]
                         )
    d2.save()
    yield db

    # optionally we can remove this but this resets to normal after test
    Donor.drop_collection()

def test_summarize_donors(testing_database):
    """given a database
    when summarize_donors is called on database
    a dict with donor summary is returned"""
    expected_result = {'test1': {'donor_name': 'test1',
                                 'total_donations': 300,
                                 'donation_count': 2,
                                 'average_donation': 150},
                       'test2': {'donor_name': 'test2',
                                 'total_donations': 300,
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
