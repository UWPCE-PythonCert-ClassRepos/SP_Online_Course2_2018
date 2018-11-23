#!/usr/bin/env python3

from peewee import *
from mailroom import Donor, Donors, Mailroom
from mailroom_model import reset_data

import os

database = SqliteDatabase('donors.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

def test_quit_menu():
    reset_data()
    mailroom = Mailroom()
    assert mailroom.quit_menu() == 'Quit'

def test_list_donors():
    reset_data()
    mailroom = Mailroom()
    assert mailroom.donors_list.list_donors().strip() == "---------- Donors ----------\nBill Ted\nFrank Fred\nLaura Todd\nSteve Lincoln\nLisa Grant"

def test_list_donations():
    reset_data()
    mailroom = Mailroom()
    donor = mailroom.donors_list.find_donor("Bill Ted")
    assert donor.list_donations().strip() == "---------- Donations by Bill Ted ----------\n353.53\n348.10\n25.00"

def test_find_donor():
    reset_data()
    mailroom = Mailroom()
    assert mailroom.donors_list.find_donor("dne") is None
    assert mailroom.donors_list.find_donor("Bill Ted") == Donor("Bill Ted")

def test_total_donations():
    reset_data()
    mailroom = Mailroom()
    donor = mailroom.donors_list.find_donor("Lisa Grant")
    assert donor.total_donations == 209.70
    donor = mailroom.donors_list.find_donor("Frank Fred")
    assert donor.total_donations == 178.76

def test_avg_donations():
    reset_data()
    mailroom = Mailroom()
    donor = mailroom.donors_list.find_donor("Lisa Grant")
    assert donor.avg_donation == 104.85
    donor = mailroom.donors_list.find_donor("Bill Ted")
    assert donor.avg_donation == 242.21

def test_num_donations():
    reset_data()
    mailroom = Mailroom()
    donor = mailroom.donors_list.find_donor("Lisa Grant")
    assert donor.num_donations == 2
    donor = mailroom.donors_list.find_donor("Frank Fred")
    assert donor.num_donations == 3

def test_name():
    reset_data()
    mailroom = Mailroom()
    donor = mailroom.donors_list.find_donor("Lisa Grant")
    assert donor.name == "Lisa Grant"
    donor = mailroom.donors_list.find_donor("Frank Fred")
    assert donor.name == "Frank Fred"

def test_donor_lt():
    reset_data()
    mailroom = Mailroom()
    donor1 = Donor("Frank Fred")
    donor2 = Donor("Lisa Grant")
    assert donor1 < donor2
    donor2 = Donor("Laura Todd")
    assert donor1 > donor2

def test_donor_eq():
    reset_data()
    mailroom = Mailroom()
    donor1 = Donor("A")
    donor2 = Donor("B")
    assert not (donor1 == donor2)
    donor2 = Donor("A")
    assert donor1 == donor2

def test_mail_everyone():
    reset_data()
    mailroom = Mailroom()
    mailroom.donors_list.mail_everyone()
    dir_files = os.listdir()
    assert 'bill_ted.txt' in dir_files
    assert 'frank_fred.txt' in dir_files
    assert 'laura_todd.txt' in dir_files
    assert 'steve_lincoln.txt' in dir_files
    assert 'lisa_grant.txt' in dir_files

    with open('bill_ted.txt') as in_file:
        file_contents = in_file.read()
        assert file_contents.strip() == ("Dear Bill Ted,\nThank you for your very generous donation of $726.63.  "
            "It \nwill go very far in supporting the Human Fund, \"Money for \nPeople.\"\n"
            "                               Sincerely\n                                      Art Vandelay")

def test_create_report():
    reset_data()
    mailroom = Mailroom()
    assert mailroom.donors_list.create_report().strip() == (
        "Donor Name          | Total Given | Num Gifts | Average Gift\n"
        "-------------------------------------------------------------\n"
        "Bill Ted            | $    726.63 |         3 | $     242.21\n"
        "Lisa Grant          | $    209.70 |         2 | $     104.85\n"
        "Frank Fred          | $    178.76 |         3 | $      59.59\n"
        "Steve Lincoln       | $    165.28 |         2 | $      82.64\n"
        "Laura Todd          | $      5.75 |         1 | $       5.75"
        )

def test_create_thank_you():
    reset_data()
    mailroom = Mailroom()
    donor = mailroom.donors_list.find_donor("Bill Ted")
    assert donor.create_thank_you(5) == ("Dear Bill Ted,\nThank you for your very generous donation of $5.00.  "
        "It \nwill go very far in supporting the Human Fund, \"Money for \nPeople.\"\n"
        "                               Sincerely\n                                      Art Vandelay")

def test_add_donation():
    reset_data()
    mailroom = Mailroom()
    assert mailroom.donors_list.add_donation("Test1", 55.55) == Donor("Test1")
    assert mailroom.donors_list.add_donation("Test1", 4) == Donor("Test1")
    assert mailroom.donors_list.add_donation("Laura Todd", 99) == Donor("Laura Todd")

database.close()
