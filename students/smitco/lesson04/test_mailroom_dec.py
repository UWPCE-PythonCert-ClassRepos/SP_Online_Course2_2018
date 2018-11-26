# lesson 04 testing for mailroom metaprogramming
# implemented using pytest
# !/usr/bin/env python3


import os
import datetime
import json
import json_save.json_save_dec as js
import mailroom_dec as m
import pytest
import sys
from unittest import mock


def test_save_data():
    ad = m.AllDonors()
    ad.add_donation("Jerry Seinfeld", 9630)
    ad.add_donation("Jerry Seinfeld", 8520)
    ad.save_data()
    test_file = open("Donor_Data.json", "r")
    assert "Jerry Seinfeld" and "[9630, 8520]" in test_file.read()

    
def test_load_data():
    ad = m.AllDonors()
    test_load = ad.load_data()
    print(test_load.donors)
    assert "Jerry Seinfeld" in test_load.donors


def test_donor_properties():
    d = m.Donor("JK Rowling", [8752])
    d.add(4862)
    assert d.total == (8752 + 4862)
    assert d.count == 2
    assert d.average == (8752 + 4862)/2

    
def test_donor_letter(capsys):
    d = m.Donor("Jim Halpert", [2685])
    print(d.get_letter_text())
    sys.stderr.write("error")
    out, err = capsys.readouterr()
    assert "Jim Halpert" and "2,685" in out

    
def test_add_donation():
    ad = m.AllDonors()
    ad.add_donation("Jim Carrey", 3425)
    assert "Jim Carrey" in ad.donors


def test_thank_yous(capsys):
    user_inputs = ["George Washington", "4295", "exit"]
    with mock.patch("builtins.input", side_effect=user_inputs):
        ad = m.AllDonors()
        ad.thank_yous()
        sys.stderr.write("error")
        out, err = capsys.readouterr()
        assert "George Washington" and "4,295" in out


def test_thank_yous_list_exit(capsys):
    user_inputs = ["List", "exit"]
    with mock.patch("builtins.input", side_effect=user_inputs):
        ad = m.AllDonors()
        ad.thank_yous()
        sys.stderr.write("error")
        out, err = capsys.readouterr()
        assert "George Washington" and "Exiting" in out


def test_thank_yous_donation_exit(capsys):
    user_inputs = ["James Bond", "exit", "list", "exit"]
    with mock.patch("builtins.input", side_effect=user_inputs):
        ad = m.AllDonors()
        ad.thank_yous()
        sys.stderr.write("error")
        out, err = capsys.readouterr()
        assert "Exiting" in out
        assert "James Bond" not in out   


def test_thank_yous_large_donation(capsys):
    user_inputs = ["James Bond", "42954356804343", "list", "exit"]
    with mock.patch("builtins.input", side_effect=user_inputs):
        ad = m.AllDonors()
        ad.thank_yous()
        sys.stderr.write("error")
        out, err = capsys.readouterr()
        assert "too large" in out
        assert "James Bond" not in out


def test_thank_yous_invalid_entry(capsys):
    user_inputs = ["James Bond", "sdhfdhfd", "list", "exit"]
    with mock.patch("builtins.input", side_effect=user_inputs):
        ad = m.AllDonors()
        ad.thank_yous()
        sys.stderr.write("error")
        out, err = capsys.readouterr()
        assert "Invalid entry" in out
        assert "James Bond" not in out


def test_get_report(capsys):
    ad = m.AllDonors()
    ad.add_donation("Joe Montana", 9520)
    ad.add_donation("Joe Montana", 7560)
    ad.get_report()
    sys.stderr.write("error")
    out, err = capsys.readouterr()
    assert "Joe Montana" in out
    assert "17,080.00" in out


def test_send_letters():
    ad = m.AllDonors()
    ad.add_donation("John Wick", 6483)
    ad.send_letters()
    current = datetime.datetime.now()
    date = [str(current.month), str(current.day), str(current.year)]
    current_date = "_".join(date)
    letter_name = ("John Wick" + " " + current_date + ".txt")
    test_file = open(letter_name, "r")
    assert "John Wick" and "6,483" in test_file.read()


def test_match(capsys):
    user_inputs = ["3000", "4000", "3"]
    with mock.patch("builtins.input", side_effect=user_inputs):
        ad = m.AllDonors()
        ad.add_donation("Jessica Biel", 3500)
        ad.match()
        sys.stderr.write("error")
        out, err = capsys.readouterr()
        assert "3,500" in out
        assert "10,500" in out


def test_quit():
    with pytest.raises(SystemExit) as py_se:
        ad = m.AllDonors()
        ad.quit()
    assert py_se.type == SystemExit