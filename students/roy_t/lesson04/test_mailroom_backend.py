#!/usr/bin/env python3

__author__ = 'roy_t'

import unittest
import mailroom_backend as mb
import os, os.path


class TestMailroomBackend(unittest.TestCase):

    def setUp(self):
        self.coll = mb.DonorCollection()
        self.coll.add_donor(mb.Donor('Fred Flintstonebanks', [27.14, 89.14]))
        self.coll.add_donor(mb.Donor('Wilma Willbanksstone', [250, 24, 57, 175]))
        self.coll.add_donor(mb.Donor('Barney Rubblemcfuddle', 150))
        self.new_donor = mb.Donor('Frankie Frankerton', [250, 1000, 1000])

    def new_donor_coll_instance_created(self):
        assert isinstance(self.coll, mb.DonorCollection)

    def new_donor_can_be_added(self):
        self.coll.add_donor(self.new_donor)
        assert self.new_donor in self.coll.donors

    def test_str_function_returns_expected_value(self):
        self.assertEqual('Donor name: Frankie Frankerton  Donations: 2250',
                         self.new_donor.__str__())

    def test_verify_file_is_saved(self):
        with self.assertRaises(FileNotFoundError):
            self.coll.save_emails('/asdfasd/asdfasdfasdsf')

        with self.assertRaises(OSError):
            self.coll.save_emails('C:\root/')
        with open(self.new_donor.name + '.txt', 'w+') as f:
            f.write(self.new_donor.letter)

        read_file = open(self.new_donor.name + '.txt', 'r')
        self.assertEqual(read_file.read(), str(self.new_donor.letter))
        read_file.close()
        if os.path.isfile(self.new_donor.name + '.txt'):
            pass
        else:
            raise FileNotFoundError

    def test_max_donations_returned(self):
        max_donation = self.new_donor.max_donation
        self.assertEqual(max_donation, 1000)

    def test_num_gifts_returned(self):
        num_gifts = len(self.new_donor.donations)
        self.assertEqual(num_gifts, 3)

    # def test_print_challenge_results(self):
    #     self.new_coll = self.coll
    #     result = self.new_coll.challenge(2)
    #     for donor in result.donors:
    #         print(donor)
    #
    # def test_donations_multiplied_correctly(self):
    #     # Verify Wilma has one donation equal to $150
    #     wilma_donations = self.coll.donors['Wilma Willbanksstone'].all_donations
    #     self.assertEqual(sum(wilma_donations), 150)
    #     self.assertEqual(len(wilma_donations), 1)
    #     multiplier = 4
    #     self.challenge_coll = self.coll.challenge(multiplier)
    #     self.assertEqual(sum(self.challenge_coll.donors['Wilma Willbanksstone'].all_donations), 600)

    def test_donor_collection_can_save_to_and_load_from_json_file(self):
        self.coll.load_json()
        assert(os.path.isfile('donorsDB.json'))
        with open('donorsDB.json', 'r') as f:
            text = f.read()
            # verify all of the donor names appear in the json output
            for d in self.coll.donors:
                self.assertTrue(d.name in text)
        self.coll.load_json()


if __name__ == "__main__":
    unittest.main()