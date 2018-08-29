#!/usr/bin/env python

# #############################################################################
# Written By: Mayc4t
# June 03, 2018
# Self-paced Python
# lesson 9
# fileID: test_mailroom5.py
# #############################################################################


import mailroom5 as mr
import unittest
import json_save.json_save.json_save_meta as js


class TestMailroom(unittest.TestCase):

    # test DONOR CLASS
    def test_donor_json(self):
        # Create a donor.
        dn = mr.Donor("Test", "Person", [100, 100, 100])

        # Create a 2nd donor using JasonSavable magic.
        dn_json = dn.to_json_compat()
        dn2 = mr.Donor.from_json_dict(dn_json)

        # Check that the donors are the same.
        self.assertEqual(dn, dn2)

    def test_donor_db_json(self):
        d1 = mr.Donor("Apple", "First", [10, 10])
        d2 = mr.Donor("Mango", "Second", [5, 5])
        db = mr.Donor_DB([d1, d2])

        db_json = db.to_json_compat()
        db2 = mr.Donor_DB.from_json_dict(db_json)

        # Check that the donors are the same.
        self.assertEqual(db, db2)

    def test_donor_db_json_text(self):
        d1 = mr.Donor("Apple", "First", [10, 10])
        d2 = mr.Donor("Mango", "Second", [5, 5])
        db = mr.Donor_DB([d1, d2])

        db2 = js.from_json(db.to_json())

        # Check that the donors are the same.
        self.assertEqual(db, db2)

    def test_donor_db_json_file(self):
        d1 = mr.Donor("Apple", "First", [10, 10])
        d2 = mr.Donor("Mango", "Second", [5, 5])
        db = mr.Donor_DB([d1, d2])

        with open('donor_db.json', 'w') as f:
            f.write(db.to_json())

        with open('donor_db.json') as f:
          db2 = js.from_json(f.read())

        # Check that the donors are the same.
        self.assertEqual(db, db2)


if __name__ == "__main__":
    unittest.main()
