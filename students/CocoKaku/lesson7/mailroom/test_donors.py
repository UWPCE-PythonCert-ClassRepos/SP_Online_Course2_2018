"""
updated tests for Python 220 Lesson 7 assignment (relational databases)
"""
from donors_model import *
import os


def setup_function():
    if os.path.isfile('test.db'): os.remove('test.db')
    database.init('test.db')
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')
    database.create_tables([Donor, Donation])
    logging.basicConfig(level=logging.ERROR)


def teardown_function():
    database.close()
    os.remove('test.db')


def test_donation_list_donors_empty_db():
    expected = ""
    assert Donation.list_donors() == expected


def test_donation_summary_report_empty_db():
    expected = "DONOR NAME             TOTAL DONATED   NUM DONATIONS   AVG DONATION\n"
    assert Donation.summary_report() == expected


def test_donation_add_donation():
    Donation.add_donation("Ann", 1)
    assert Donor.get(name="Ann").name == "Ann"
    assert Donation.get(name="Ann").name.name == "Ann"
    assert Donation.get(name="Ann").amount == 1


def test_donation_list_donors_one_donor_one_donation():
    Donation.add_donation("Ann", 1)
    assert Donation.list_donors() == "   Ann"


def test_donors_summary_report_one_name_one_value():
    Donation.add_donation("Ann", 1)
    expected = "DONOR NAME             TOTAL DONATED   NUM DONATIONS   AVG DONATION\n" \
               "Ann                    $        1.00   1               $       1.00\n"
    assert Donation.summary_report() == expected


def test_donation_list_donors_one_donor_plusone_donation():
    Donation.add_donation("Ann", 1)
    Donation.add_donation("Ann", 1.1)
    assert Donation.list_donors() == "   Ann"


def test_donation_summary_report_one_name_multiple_values():
    Donation.add_donation("Ann", 1)
    Donation.add_donation("Ann", 1.1)
    expected = "DONOR NAME             TOTAL DONATED   NUM DONATIONS   AVG DONATION\n" \
               "Ann                    $        2.10   2               $       1.05\n"
    assert Donation.summary_report() == expected


def test_donation_thank_you_letter():
    Donation.add_donation("Bill", 300)
    expected = f"Dear Bill,\n" \
               f"Thank you very much for your generous donation of $300.00.\n" \
               f"Sincerely,\n" \
               f"PYTHON220 Class of 2019"
    assert Donation.thank_you_letter("Bill") == expected


def test_donation_thank_you_letter_multiple_donations():
    Donation.add_donation("Joe", 100)
    Donation.add_donation("Joe", 200)
    expected = f"Dear Joe,\n" \
               f"Thank you very much for your generous donation of $200.00.\n" \
               f"Sincerely,\n" \
               f"PYTHON220 Class of 2019"
    assert Donation.thank_you_letter("Joe") == expected



def test_donation_summary_report_multiple_names_multiple_values():
    Donation.add_donation("Ann", 1)
    Donation.add_donation("Ann", 1.1)
    Donation.add_donation("Bill", 300)
    Donation.add_donation("Joe", 100)
    Donation.add_donation("Joe", 200)
    expected = "DONOR NAME             TOTAL DONATED   NUM DONATIONS   AVG DONATION\n" \
               "Bill                   $      300.00   1               $     300.00\n" \
               "Joe                    $      300.00   2               $     150.00\n" \
               "Ann                    $        2.10   2               $       1.05\n"
    assert Donation.summary_report() == expected


# tests for donors challenge
def test_donation_challenge():
    Donation.add_donation("Ann", 1)
    Donation.add_donation("Ann", 2)
    Donation.add_donation("Ann", 3)
    Donation.add_donation("Barry", 4)
    Donation.add_donation("Barry", 5)
    Donation.add_donation("Barry", 6)
    expected = "   Ann: $12.00 = 2 * $6.00\n" \
               "   Barry: $30.00 = 2 * $15.00\n" \
               "\n   Total contribution required: $42.00\n"
    assert Donation.challenge(2) == expected

def test_donors_challenge_min_donation():
    Donation.add_donation("Ann", 1)
    Donation.add_donation("Ann", 2)
    Donation.add_donation("Ann", 3)
    Donation.add_donation("Barry", 4)
    Donation.add_donation("Barry", 5)
    Donation.add_donation("Barry", 6)
    expected = "   Barry: $30.00 = 2 * $15.00\n" \
               "\n   Total contribution required: $30.00\n"
    assert Donation.challenge(2, min_donation=4) == expected


def test_donation_challenge_max_donation():
    Donation.add_donation("Ann", 1)
    Donation.add_donation("Ann", 2)
    Donation.add_donation("Ann", 3)
    Donation.add_donation("Barry", 4)
    Donation.add_donation("Barry", 5)
    Donation.add_donation("Barry", 6)
    expected = "   Ann: $12.00 = 2 * $6.00\n" \
               "   Barry: $8.00 = 2 * $4.00\n" \
               "\n   Total contribution required: $20.00\n"
    assert Donation.challenge(2, max_donation=4) == expected


def test_donation_challenge_min_and_max_donation():
    Donation.add_donation("Ann", 1)
    Donation.add_donation("Ann", 2)
    Donation.add_donation("Ann", 3)
    Donation.add_donation("Barry", 4)
    Donation.add_donation("Barry", 5)
    Donation.add_donation("Barry", 6)
    expected = "   Ann: $10.00 = 2 * $5.00\n" \
               "   Barry: $18.00 = 2 * $9.00\n" \
               "\n   Total contribution required: $28.00\n"
    assert Donation.challenge(2, min_donation=2, max_donation=5) == expected


def test_donation_delete_donation():
    Donation.add_donation("Ann", 3)
    Donation.add_donation("Ann", 2)
    Donation.add_donation("Bill", 2)
    Donation.add_donation("Joe", 1)
    Donation.add_donation("Joe", 1)
    op1 = Donation.delete_donation("Bill", 2)
    op2 = Donation.delete_donation("Ann", 2)
    op3 = Donation.delete_donation("Bill", 2)
    expected = "DONOR NAME             TOTAL DONATED   NUM DONATIONS   AVG DONATION\n" \
               "Ann                    $        3.00   1               $       3.00\n" \
               "Joe                    $        2.00   2               $       1.00\n"
    assert Donation.summary_report() == expected
    assert op1
    assert op2
    assert not op3


def test_donation_delete_donor():
    Donation.add_donation("Ann", 3)
    Donation.add_donation("Ann", 2)
    Donation.add_donation("Bill", 2)
    Donation.add_donation("Joe", 1)
    Donation.add_donation("Joe", 1)
    op1 = Donation.delete_donor("Bill")
    op2 = Donation.delete_donor("Joe")
    op3 = Donation.delete_donor("Clancy")
    expected = "DONOR NAME             TOTAL DONATED   NUM DONATIONS   AVG DONATION\n" \
               "Ann                    $        5.00   2               $       2.50\n"
    assert Donation.summary_report() == expected
    assert op1
    assert op2
    assert not op3


def test_donation_update_donation():
    Donation.add_donation("Ann", 3)
    Donation.add_donation("Ann", 2)
    Donation.add_donation("Bill", 2)
    Donation.add_donation("Joe", 1)
    Donation.add_donation("Joe", 1)
    op1 = Donation.update_donation("Bill", 2, 4)
    op2 = Donation.update_donation("Joe", 1, 2)
    op3 = Donation.update_donation("Clancy", 2, 3)
    expected = "DONOR NAME             TOTAL DONATED   NUM DONATIONS   AVG DONATION\n" \
               "Ann                    $        5.00   2               $       2.50\n" \
               "Bill                   $        4.00   1               $       4.00\n" \
               "Joe                    $        3.00   2               $       1.50\n"
    assert Donation.summary_report() == expected
    assert op1
    assert op2
    assert not op3


def test_donation_update_donor():
    Donation.add_donation("Ann", 3)
    Donation.add_donation("Ann", 2)
    Donation.add_donation("Bill", 2)
    Donation.add_donation("Joe", 1)
    Donation.add_donation("Joe", 1)
    op1 = Donation.update_donor("Bill", "Bolliver")
    op2 = Donation.update_donor("Joe", "Ann")
    op3 = Donation.update_donor("Clancy", "Cleaver")
    expected = "DONOR NAME             TOTAL DONATED   NUM DONATIONS   AVG DONATION\n" \
               "Ann                    $        5.00   2               $       2.50\n" \
               "Bolliver               $        2.00   1               $       2.00\n" \
               "Joe                    $        2.00   2               $       1.00\n"
    assert Donation.summary_report() == expected
    assert op1
    assert not op2
    assert not op3

    pass