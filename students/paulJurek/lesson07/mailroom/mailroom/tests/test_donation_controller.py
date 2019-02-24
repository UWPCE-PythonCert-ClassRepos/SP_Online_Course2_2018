"""testing the donation controller for donation center"""

import datetime
import pathlib
import pytest
from mailroom.Donor import Donor
from mailroom.DonationController import DonationController

@pytest.fixture
def donation_controller():
    """sample controller for save the whales foundation
    setup with basic information and no donations"""
    return DonationController(name='Save The Whales')

# TODO: get rid of donor fixtures.  These should not be part of unit tests here
# use mock
@pytest.fixture
def donor1():
    return Donor(id=1, firstname='Fisher', lastname='Price')

# TODO: get rid of donor fixtures.  These should not be part of unit tests here
# use mock
@pytest.fixture
def donor2():
    return Donor(id=2, firstname='Wonky', lastname='Donkey')

# TODO: change to point to sqlite
# TODO: update tests to only test controller save
def test_controller_creates_saved_file(donation_controller, donor1):
    """given a controller is intialized and donors added
    when saved with the internal method and then loaded
    then the results can be reloaded"""
    # create controller and save
    test_filename = 'test.json'
    donation_controller.create_donor(donor1)
    extract = donation_controller.save(test_filename)

    # now make load database and compare
    donation_controller2 = DonationController.load(test_filename)
    assert str(donation_controller) == str(donation_controller2)

# TODO: update with mock
def test_create_new_donor(donation_controller, donor1):
    """given a donation controller
    when user creates new donor
    the user is added to the donation controller"""
    assert donation_controller.find_donor(donor1) is None
    donation_controller.create_donor(donor1)
    assert donation_controller.find_donor(donor1) == donor1

# TODO: update with mock
def test_create_new_donor_creates_error_if_exists(donation_controller, donor1):
    donation_controller.create_donor(donor1)
    assert donation_controller.find_donor(donor1) == donor1

    with pytest.raises(KeyError):
        donation_controller.create_donor(donor1)

# TODO: update with mock
def test_create_donation_for_donor(donation_controller, donor1):
    """given a controller and donor
    when a donation is added to donor
    the controller's total is updated"""
    assert donation_controller.get_total_donations() == 0
    donation_controller.create_donor(donor1)
    donation_controller.create_donation(donor=donor1, amount=500)
    assert donation_controller.get_total_donations() == 500

def test_error_when_create_donation_for_missing_donor(donation_controller, donor1):
    """give user tries to add donation for non-existanant donor
    when the amount is applied
    an exception is returned"""
    with pytest.raises(IndexError):
        donation_controller.create_donation(donor=donor1, amount=500)

def test_send_letters_to_all_donors(donation_controller, donor1, donor2, tmpdir):
    """given controller
    when triggers send letters to donors
    letters are sent to all donors as indicated by letters being generated"""
    # ensure no letters are avaliable
    assert len(tmpdir.listdir())==0

    # create donors
    donation_controller.create_donor(donor1)
    donation_controller.create_donation(donor=donor1, amount=500)
    donation_controller.create_donor(donor2)
    donation_controller.create_donation(donor=donor2, amount=5)

    # verify we have donors otherwise last assert will fail
    donation_controller.send_letters_to_everyone(thank_you_directory=tmpdir)
    assert len(tmpdir.listdir()) > 0

def test_next_id_property(donation_controller, donor1, donor2):
        """tests next id show correct details
        given a blank donor collection
        when next_id called
        1 is returned"""
        assert donation_controller.next_id == 1

        """given a blank donor collection
        when two donors are added and next_id called
        integer above max is returned"""
        donation_controller.create_donor(donor2)
        assert donation_controller.next_id == 1

        donation_controller.create_donor(donor1)
        assert donation_controller.next_id == 3

def test_controller_challege_errors_on_small_value(donation_controller):
        """given controller
        when challenge raised with value less than 1
        error raised"""

        with pytest.raises(ValueError):
                donation_controller.challenge(0.1)

def test_challenge_increase_donation_total(donation_controller, donor1, donor2):
        """given donation controller
        when challenge applied
        new controller has increased donation amount"""
        FACTOR = 2
        # create donors
        donation_controller.create_donor(donor1)
        donation_controller.create_donation(donor=donor1, amount=500)
        donation_controller.create_donor(donor2)
        donation_controller.create_donation(donor=donor2, amount=5)

        trees = donation_controller.challenge(FACTOR)
        assert donation_controller.get_total_donations() * FACTOR == trees.get_total_donations()

def test_challenge_increase_large_donations(donation_controller, donor1, donor2):
        """given donation controller
        when challenge applied
        new controller has increased donation amount"""
        FACTOR = 2
        # create donors
        donation_controller.create_donor(donor1)
        donation_controller.create_donation(donor=donor1, amount=500)
        donation_controller.create_donor(donor2)
        donation_controller.create_donation(donor=donor2, amount=5)

        trees = donation_controller.challenge(FACTOR, min_donation = 100)
        assert trees.get_total_donations() == 1000

def test_challenge_increase_small_donations(donation_controller, donor1, donor2):
        """given donation controller
        when challenge applied
        new controller has increased donation amount"""
        FACTOR = 2
        # create donors
        donation_controller.create_donor(donor1)
        donation_controller.create_donation(donor=donor1, amount=500)
        donation_controller.create_donor(donor2)
        donation_controller.create_donation(donor=donor2, amount=5)

        trees = donation_controller.challenge(FACTOR, max_donation=100)
        assert trees.get_total_donations() == 10

def test_projecting_donation(donation_controller, donor1, donor2):
        """given donation controller with some donors
        when projection created
        total amount pressented to user for what they would need to contribute"""
        FACTOR = 2
        donation_controller.create_donor(donor1)
        for i in range(1, 13):
                if i % 2:
                        donation_amount = 50
                else:
                        donation_amount = 500
                donation_controller.create_donation(donor=donor1, amount=donation_amount, date=datetime.datetime(2018,i,1))

        assert donation_controller.project_donation(factor=FACTOR, min_donation=0, max_donation=5000)==3300*FACTOR
