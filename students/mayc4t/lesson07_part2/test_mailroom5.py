#!/usr/bin/env python

# #############################################################################
# Written By: Mayc4t
# June 03, 2018
# Self-paced Python
# lesson 9
# fileID: test_mailroom5.py
# #############################################################################

import os.path
import unittest

import builtins
db_name = 'TEST_ONLY_mailroom5_FAKE_DONORS.db'
builtins.model_py_database_name_for_mailroom5_donors = db_name
import model
import mailroom5 as mr


donors = [
    ('Wolverine', 'Smith'),
    ('Stormy', 'Ocean'),
    ('Super', 'Woman'),
    ('Bob', 'Gambino'),
]


donations = {
    'Smith,Wolverine': [199.99, 50, 1.01],
    'Ocean,Stormy': [10, 100],
    'Woman,Super': [20.05],
    'Gambino,Bob': [1, 2, 3, 4],
}


class TestMailroom(unittest.TestCase):

    def setUp(self):
        if os.path.exists(db_name):
            os.remove(db_name)

    def tearDown(self):
        if os.path.exists(db_name):
            os.remove(db_name)

    def test_create_tables(self):
        model.CreateTables()

        # Assert that the .db file got created
        self.assertTrue(os.path.isfile(db_name)) 


    def test_save_donor_info(self):
        self.test_create_tables()
        
        for donor in donors:
            model.SaveDonorInfo(donor[0], donor[1])

        try:
            model.database.connect()
            model.database.execute_sql('PRAGMA foreign_keys = ON;')
            for want, got in zip(donors, model.DonorInfo):
                self.assertEqual(want[1] + ',' + want[0], got.name)
                self.assertEqual(want[0], got.first_name)
                self.assertEqual(want[1], got.last_name)
        except Exception as e:
            self.assertTrue(False)
        finally:
            model.database.close()

    def test_save_donation(self):
        self.test_save_donor_info()

        for name, donation_list in donations.items():
            for donation in donation_list:
                model.SaveDonation(name, donation)

        try:
            model.database.connect()
            model.database.execute_sql('PRAGMA foreign_keys = ON;')

            for name, donation_list in donations.items():
                query = (model.Donation
                         .select()
                         .join(model.DonorInfo)
                         .where(model.Donation.donor == name))
                for want, got in zip(donation_list, query):
                    self.assertEqual(want, got.donation)
        except Exception as e:
            self.assertTrue(False)
        finally:
            model.database.close()


if __name__ == "__main__":
    unittest.main()
