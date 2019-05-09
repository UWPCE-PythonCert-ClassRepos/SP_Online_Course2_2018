"""
updated tests for Python 220 Lesson 7 assignment (relational databases)
"""

from donors_model import *
import pytest
import utilities
import os


log = utilities.configure_logger('default', 'logs/login_databases_dev.log')


@pytest.fixture(scope='module')
def test_db():
    test_db = Donations('test_db')
    yield test_db
    log.info('Close connection')
    test_db.close_db()


@pytest.fixture(autouse=True)
def setup_function(test_db):
    test_db.clear_db()

def test_donation_list_donors_empty_db(test_db):
    expected = ""
    assert test_db.list_donors() == expected


def test_donation_summary_report_empty_db(test_db):
    expected = "DONOR NAME             TOTAL DONATED   NUM DONATIONS   AVG DONATION\n"
    assert test_db.summary_report() == expected


def test_donation_add_donation(test_db):
    test_db.add_donation("Ann", 1)
    query = test_db.mycol.find_one({'name': 'Ann'}, sort=[('_id', pymongo.DESCENDING)])
    assert query['name'] == "Ann"
    assert query['amount'] == 1


def test_donation_list_donors_one_donor_one_donation(test_db):
    test_db.add_donation("Ann", 1)
    assert test_db.list_donors() == "   Ann"


def test_donors_summary_report_one_name_one_value(test_db):
    test_db.add_donation("Ann", 1)
    expected = "DONOR NAME             TOTAL DONATED   NUM DONATIONS   AVG DONATION\n" \
               "Ann                    $        1.00   1               $       1.00\n"
    assert test_db.summary_report() == expected


def test_donation_list_donors_one_donor_plusone_donation(test_db):
    test_db.add_donation("Ann", 1)
    test_db.add_donation("Ann", 1.1)
    assert test_db.list_donors() == "   Ann"


def test_donation_summary_report_one_name_multiple_values(test_db):
    test_db.add_donation("Ann", 1)
    test_db.add_donation("Ann", 1.1)
    expected = "DONOR NAME             TOTAL DONATED   NUM DONATIONS   AVG DONATION\n" \
               "Ann                    $        2.10   2               $       1.05\n"
    assert test_db.summary_report() == expected


def test_donation_thank_you_letter(test_db):
    test_db.add_donation("Bill", 300)
    expected = f"Dear Bill,\n" \
               f"Thank you very much for your generous donation of $300.00.\n" \
               f"Sincerely,\n" \
               f"PYTHON220 Class of 2019"
    assert test_db.thank_you_letter("Bill") == expected


def test_donation_thank_you_letter_multiple_donations(test_db):
    test_db.add_donation("Joe", 100)
    test_db.add_donation("Joe", 200)
    expected = f"Dear Joe,\n" \
               f"Thank you very much for your generous donation of $200.00.\n" \
               f"Sincerely,\n" \
               f"PYTHON220 Class of 2019"
    assert test_db.thank_you_letter("Joe") == expected



def test_donation_summary_report_multiple_names_multiple_values(test_db):
    test_db.add_donation("Ann", 1)
    test_db.add_donation("Ann", 1.1)
    test_db.add_donation("Bill", 300)
    test_db.add_donation("Joe", 100)
    test_db.add_donation("Joe", 200)
    expected = "DONOR NAME             TOTAL DONATED   NUM DONATIONS   AVG DONATION\n" \
               "Bill                   $      300.00   1               $     300.00\n" \
               "Joe                    $      300.00   2               $     150.00\n" \
               "Ann                    $        2.10   2               $       1.05\n"
    assert test_db.summary_report() == expected


# tests for donors challenge
def test_donation_challenge(test_db):
    test_db.add_donation("Ann", 1)
    test_db.add_donation("Ann", 2)
    test_db.add_donation("Ann", 3)
    test_db.add_donation("Barry", 4)
    test_db.add_donation("Barry", 5)
    test_db.add_donation("Barry", 6)
    expected = "   Ann: $12.00 = 2 * $6.00\n" \
               "   Barry: $30.00 = 2 * $15.00\n" \
               "\n   Total contribution required: $42.00\n"
    assert test_db.challenge(2) == expected

def test_donors_challenge_min_donation(test_db):
    test_db.add_donation("Ann", 1)
    test_db.add_donation("Ann", 2)
    test_db.add_donation("Ann", 3)
    test_db.add_donation("Barry", 4)
    test_db.add_donation("Barry", 5)
    test_db.add_donation("Barry", 6)
    expected = "   Barry: $30.00 = 2 * $15.00\n" \
               "\n   Total contribution required: $30.00\n"
    assert test_db.challenge(2, min_donation=4) == expected


def test_donation_challenge_max_donation(test_db):
    test_db.add_donation("Ann", 1)
    test_db.add_donation("Ann", 2)
    test_db.add_donation("Ann", 3)
    test_db.add_donation("Barry", 4)
    test_db.add_donation("Barry", 5)
    test_db.add_donation("Barry", 6)
    expected = "   Ann: $12.00 = 2 * $6.00\n" \
               "   Barry: $8.00 = 2 * $4.00\n" \
               "\n   Total contribution required: $20.00\n"
    assert test_db.challenge(2, max_donation=4) == expected


def test_donation_challenge_min_and_max_donation(test_db):
    test_db.add_donation("Ann", 1)
    test_db.add_donation("Ann", 2)
    test_db.add_donation("Ann", 3)
    test_db.add_donation("Barry", 4)
    test_db.add_donation("Barry", 5)
    test_db.add_donation("Barry", 6)
    expected = "   Ann: $10.00 = 2 * $5.00\n" \
               "   Barry: $18.00 = 2 * $9.00\n" \
               "\n   Total contribution required: $28.00\n"
    assert test_db.challenge(2, min_donation=2, max_donation=5) == expected


def test_donation_delete_donation(test_db):
    test_db.add_donation("Ann", 3)
    test_db.add_donation("Ann", 2)
    test_db.add_donation("Bill", 2)
    test_db.add_donation("Joe", 1)
    test_db.add_donation("Joe", 1)
    op1 = test_db.delete_donation("Bill", 2)
    op2 = test_db.delete_donation("Ann", 2)
    op3 = test_db.delete_donation("Bill", 2)
    expected = "DONOR NAME             TOTAL DONATED   NUM DONATIONS   AVG DONATION\n" \
               "Ann                    $        3.00   1               $       3.00\n" \
               "Joe                    $        2.00   2               $       1.00\n"
    assert test_db.summary_report() == expected
    assert op1
    assert op2
    assert not op3


def test_donation_delete_donor(test_db):
    test_db.add_donation("Ann", 3)
    test_db.add_donation("Ann", 2)
    test_db.add_donation("Bill", 2)
    test_db.add_donation("Joe", 1)
    test_db.add_donation("Joe", 1)
    op1 = test_db.delete_donor("Bill")
    op2 = test_db.delete_donor("Joe")
    op3 = test_db.delete_donor("Clancy")
    expected = "DONOR NAME             TOTAL DONATED   NUM DONATIONS   AVG DONATION\n" \
               "Ann                    $        5.00   2               $       2.50\n"
    assert test_db.summary_report() == expected
    assert op1
    assert op2
    assert not op3


def test_donation_update_donation(test_db):
    test_db.add_donation("Ann", 3)
    test_db.add_donation("Ann", 2)
    test_db.add_donation("Bill", 2)
    test_db.add_donation("Joe", 1)
    test_db.add_donation("Joe", 1)
    op1 = test_db.update_donation("Bill", 2, 4)
    op2 = test_db.update_donation("Joe", 1, 2)
    op3 = test_db.update_donation("Clancy", 2, 3)
    expected = "DONOR NAME             TOTAL DONATED   NUM DONATIONS   AVG DONATION\n" \
               "Ann                    $        5.00   2               $       2.50\n" \
               "Bill                   $        4.00   1               $       4.00\n" \
               "Joe                    $        3.00   2               $       1.50\n"
    assert test_db.summary_report() == expected
    assert op1
    assert op2
    assert not op3


def test_donation_update_donor(test_db):
    test_db.add_donation("Ann", 3)
    test_db.add_donation("Ann", 2)
    test_db.add_donation("Bill", 2)
    test_db.add_donation("Joe", 1)
    test_db.add_donation("Joe", 1)
    op1 = test_db.update_donor("Bill", "Bolliver")
    op2 = test_db.update_donor("Joe", "Ann")
    op3 = test_db.update_donor("Clancy", "Cleaver")
    expected = "DONOR NAME             TOTAL DONATED   NUM DONATIONS   AVG DONATION\n" \
               "Ann                    $        5.00   2               $       2.50\n" \
               "Bolliver               $        2.00   1               $       2.00\n" \
               "Joe                    $        2.00   2               $       1.00\n"
    assert test_db.summary_report() == expected
    assert op1
    assert not op2
    assert not op3
