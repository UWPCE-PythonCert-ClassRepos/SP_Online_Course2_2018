"""testing the donation controller for donation center"""

import datetime
import pathlib
import pytest
from mailroom.DonationController import DonationController
from mailroom.Donor import Donor
from mailroom.Donation import Donation
from mailroom.config import database

@pytest.fixture
def donation_controller():
    """sample controller for save the whales foundation
    setup with basic information and no donations"""
    database.connect()
    database.create_tables([Donor, Donation])
    yield DonationController()
    database.close()


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


# TODO: update with mock
def test_create_donation_for_donor(donation_controller):
    """given a controller and donor
    when a donation is added to donor
    the controller's total is updated"""
    donation_amount = 500
    donor = 'test1'
    donation = donation_controller.create_donation(amount= donation_amount, donor='SantaClause')
    assert donation.donation_amount == donation_amount

def test_error_when_create_donation_for_missing_donor(donation_controller):
    """give user tries to add donation for non-existanant donor
    when the amount is applied
    an exception is returned"""
    donor = 'not a donor'
    if donation_controller.find_donor(donor):
        donation_controller.create_donation(donor='not a donor', amount=500)
    else:
        donation_controller.create_donor(donor_name=donor)
