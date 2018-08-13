#!/usr/bin/env python3

import mailroom_json as mj
import json
import json_save.json_save_dec as js
import sys
import string
import os.path
from collections import defaultdict


Luke = mj.DonorHistory('Luke Rodriguez', [5512.75, 3250.50, 42.50])
River = mj.DonorHistory('River Tails', [63.00, 1200.00, 300.00, 450.00, 4000.00])
Virgil = mj.DonorHistory('Virgil Ferdinand', [350.00, 5000.00])
Jokib = mj.DonorHistory('Joseph Kibson', [3498.00, 5.50])
mailroom = mj.Roster([Luke, River, Virgil, Jokib])

'''def test_donor_list():
    mail_list = mj.donor_report()
    assert "Luke" in mail_list
    assert "River" in mail_list
    assert "Virgil" in mail_list
    assert "Jokib" in mail_list'''


def test_donor_report():
    report = mailroom.donor_report()
    assert 'Luke' in report
    assert 'River' in report
    assert 'Virgil' in report
    assert 'Joseph' in report

def test_write_files():
    mailroom.write_files()
    assert os.path.isfile("Luke.txt")
    assert os.path.isfile("River.txt")
    assert os.path.isfile("Virgil.txt")
    assert os.path.isfile("Jokib.txt")

def test_save():
    mailroom.save_roster()
    assert os.path.isfile("roster.json")

def test_load():
    with open('test_roster.json', 'r') as roster_json:
        roster = roster_json.read()
        roster_dict = json.loads(roster)
        mailroom = mj.Roster.from_json_dict(roster_dict)
    report = mailroom.donor_report()
    assert 'Luke' in report
    mailroom.write_files()
    assert os.path.isfile("Luke.txt")

if __name__ == "__main__":


    test_donor_report()
    test_write_files()
    test_save()
    test_load()