#!/usr/bin/env python3

import mailroom_json as mr
import json
import json_save.json_save_dec as js
import sys
import string
import os.path
from collections import defaultdict


Andy = mr.Donor('Andy', [10.00])
Bill = mr.Donor('Bill', [15.00, 25.00])
Chuck = mr.Donor('Chuck', [20.00, 30.00, 40.00])
mailroom = mr.Roster([Andy, Bill, Chuck])

'''def test_donor_list():
    mail_list = mailroom.donor_report()
    assert "Andy" in mail_list
    assert "Bill" in mail_list
    assert "Chuck" in mail_list'''


def test_donor_report():
    report = mailroom.donor_report()
    assert 'Andy' in report
    assert 'Bill' in report
    assert 'Chuck' in report


def test_batch_file():
    mailroom.batch_file()
    assert os.path.isfile("Andy.txt")
    assert os.path.isfile("Bill.txt")
    assert os.path.isfile("Chuck.txt")

def test_save():
    mailroom.save_roster()
    assert os.path.isfile("roster.json")

def test_load():
    with open('test_roster.json', 'r') as roster_json:
        roster = roster_json.read()
        roster_dict = json.loads(roster)
        mailroom = mr.Roster.from_json_dict(roster_dict)
    report = mailroom.donor_report()
    assert 'Dave' in report
    mailroom.batch_file()
    assert os.path.isfile("Dave.txt")

if __name__ == "__main__":


    test_donor_report()
    test_batch_file()
    test_save()
    test_load()
