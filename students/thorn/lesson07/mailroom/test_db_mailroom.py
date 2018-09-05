'''
Tests for db_mailroom.py
'''

import os
import db_mailroom

tester = db_mailroom.Donor("Test Person", [1, 2, 3])
tester2 = db_mailroom.Donor("Test2 Person2", [4, 5, 6])
test_donors = db_mailroom.DonorList([tester, tester2])

def test_name():
    assert tester.name == "Test Person"

def test_first_donations():
    assert tester.donations == [1, 2, 3]

def test_donor_totals():
    assert tester.donor_totals == 6

def test_add_donations():
    add_tester = db_mailroom.Donor("Test Person", [1, 2, 3])
    add_tester.add_donation(4)
    assert add_tester.donations == [1, 2, 3, 4]
    assert add_tester.donor_totals == 10

def test_num_donations():
    assert tester.num_donations == 3

def test_average_donations():
    assert tester.average_donations == 2

def test_list_donor_names():
    assert test_donors.list_donor_names() == "Test Person\nTest2 Person2"

def test_add_donor():
    tester = db_mailroom.Donor("Test Person", [1, 2, 3])
    tester2 = db_mailroom.Donor("Test2 Person2", [4, 5, 6])
    test_donors = db_mailroom.DonorList([tester, tester2])
    assert test_donors.list_donor_names() == "Test Person\nTest2 Person2"
    tester3 = db_mailroom.Donor("Test3 Person3", [7, 8, 9])
    test_donors.add_donor(tester3)
    assert test_donors.list_donor_names() == "Test Person\nTest2 Person2\nTest3 Person3"
    assert tester3.num_donations == 3
    
def test_add_donation():
    test_add = db_mailroom.DonorList([tester, tester2])
    test_add.add_donation(tester, 4)
    assert tester.num_donations == 4

def test_add_donor_and_donation():
    tester = db_mailroom.Donor("Test Person", [1, 2, 3])
    tester2 = db_mailroom.Donor("Test2 Person2", [4, 5, 6])
    test_donors = db_mailroom.DonorList([tester])
    test_donors.add_donor_and_donation(tester2, 7)
    assert tester2.num_donations == 4

def test_order_donors():
    # Second person should be tester
    o_d = test_donors.order_donors()
    assert o_d[1] == [tester]
