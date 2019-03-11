"""testing the donation controller for donation center
The donation controller tests that correct calls to database
object is made but does not actually return data.  That is 
saved for integration test.  """

import datetime
import pathlib
import pytest
from pytest_mock import mocker
import sys

from mailroom.DonationController import DonationController
from mailroom.config import database

# TODO: move this out of donation controller and to integration test
@pytest.fixture
def sqlite_dbaccess():
    """setup of initial sqlite database for testing"""
    from mailroom.SqliteDatabaseLayer import SQLiteAccessLayer

    access_layer = SQLiteAccessLayer()
    access_layer.db_init(':memory:')

    yield access_layer

    access_layer.close()

# TODO: modify to not rely on database
@pytest.fixture
def donation_controller(sqlite_dbaccess):
    """sample controller for save the whales foundation
    setup with basic information and no donations"""
    yield DonationController(sqlite_dbaccess)


@pytest.mark.xfail(reason='error not implemented')
def test_error_when_create_donation_for_missing_donor(donation_controller):
    """give user tries to add donation for non-existanant donor
    when the amount is applied
    an exception is returned"""
    donor = 'not a donor'
    if donation_controller.find_donor(donor):
        donation_controller.create_donation(donor='not a donor', amount=500)
    else:
        donation_controller.create_donor(donor_name=donor)


def test_donor_report_calls_donor_summary(donation_controller, mocker):
    """given donation controller
    when user calls summarize_donors
    this command is passed to database and calls summarize_donors"""
    mocker.patch.object(donation_controller, 'database')
    donation_controller.database.summarize_donors.return_value = None
   
    donation_controller.donor_report()
    donation_controller.database.summarize_donors.assert_called_with()


def test_display_donor_donations_calls_donations(donation_controller, mocker):
    """given a donation controller
    when display_donor_donation is called
    get_donations is called from database"""
    mocker.patch.object(donation_controller, 'database')
    donation_controller.database.get_donations.return_value = None
   
    donation_controller.display_donor_donations(donor='test')
    donation_controller.database.get_donations.assert_called_with(donor='test')

def test_create_donation_calls_donations(donation_controller, mocker):
    """given a donation controller
    when display_donor_donation is called
    get_donations is called from database"""
    mocker.patch.object(donation_controller, 'database')
    donation_controller.database.create_donation.return_value = None
   
    donation_date = datetime.datetime.utcnow()
    donation_controller.create_donation(donor='test'
                                        , amount=123
                                        , date = donation_date)
    donation_controller.database.create_donation.assert_called_with(donor='test'
                                                                    , amount=123
                                                                    , date=donation_date)

def test_find_donor_calls_database_donor(donation_controller, mocker):
    """given a donation controller
    when find_donor is called
    equivalent function in database is called"""
    mocker.patch.object(donation_controller, 'database')
    donation_controller.database.find_donor.return_value = None
   
    donation_controller.find_donor(donor_name='test')
    donation_controller.database.find_donor.assert_called_with(donor_name='test')
