"""
    Unit tests for the mailroom program
"""
from .mailroom_peewee import *
from .fill_mail import populate_db, populate_donos, populate_details

from unittest import TestCase

class Mailroom_tester(TestCase):

    def setUp(self):
#        populate_db()
#        populate_donos()
#        populate_details()
        pass

    def test_01_new_donor(self):
        #this gets the next invoice number to be used
        num = (Donation.select(fn.MAX(Donation.dono_number)).scalar())
        if num == None:
            num = 0

        new_donor('New Donor', 300.0, 'Large', num)

        set_variables('New Donor')

        query = (Details.select().where(Details.name == 'New Donor'))
        query = [i for i in query][0]
        query2 = (Donation.select().where(Donation.held_by == 'New Donor'))
        dono1 = [i for i in query2][0]
        total_donations = (Donor.select().where(Donor.donor_name == 'New Donor'))
        total_donations = [i.donations for i in total_donations][0]

        NAME = 0
        DONO = 1
        DONO_SIZE = 2
        DONO_NUMBER = 3
        TRANSACTIONS = 4
        AVERAGE = 5
        FIRST_GIFT = 6
        LAST_GIFT = 7
        TOTAL_DONOS = 8

        expected = ['New Donor', 300, 'Large', (num + 1), 1, 300, 300, 300, 300]
        self.assertEqual(str(query.name), expected[NAME])
        self.assertEqual(float(dono1.dono), expected[DONO])
        self.assertEqual(str(dono1.dono_size), expected[DONO_SIZE])
        self.assertEqual(dono1.dono_number, expected[DONO_NUMBER])
        self.assertEqual(int(query.transactions), expected[TRANSACTIONS])
        self.assertEqual(float(query.average), expected[AVERAGE])
        self.assertEqual(float(query.first_gift), expected[FIRST_GIFT])
        self.assertEqual(float(query.last_gift), expected[LAST_GIFT])
        self.assertEqual(float(total_donations), expected[TOTAL_DONOS])

    def test_02_existing_donor(self):
        #this gets the next invoice number to be used

        num = (Donation.select(fn.MAX(Donation.dono_number)).scalar())
        
        existing_donor('New Donor', 500.0, 'Large', num)
        set_variables('New Donor')

        query = (Details.select().where(Details.name == 'New Donor'))
        query = [i for i in query][0]
        query2 = (Donation.select().where(Donation.held_by == 'New Donor'))
        dono1 = [i for i in query2][0]
        dono2 = [i for i in query2][1]
        total_donations = (Donor.select().where(Donor.donor_name == 'New Donor'))
        total_donations = [i.donations for i in total_donations][0]


        NAME = 0
        DONO_ONE = 1
        DONO_TWO = 2
        DONO_SIZE = 3
        DONO_NUMBER = 4
        TRANSACTIONS = 5
        AVERAGE = 6
        FIRST_GIFT = 7
        LAST_GIFT = 8
        TOTAL_DONOS = 9

        expected = ['New Donor', 300, 500, 'Large', (num + 1), 2, 400, 300, 500, 800]
        self.assertEqual(str(query.name), expected[NAME])
        self.assertEqual(float(dono1.dono), expected[DONO_ONE])
        self.assertEqual(float(dono2.dono), expected[DONO_TWO])
        self.assertEqual(str(dono2.dono_size), expected[DONO_SIZE])
        self.assertEqual(dono2.dono_number, expected[DONO_NUMBER])
        self.assertEqual(int(query.transactions), expected[TRANSACTIONS])
        self.assertEqual(float(query.average), expected[AVERAGE])
        self.assertEqual(float(query.first_gift), expected[FIRST_GIFT])
        self.assertEqual(float(query.last_gift), expected[LAST_GIFT])
        self.assertEqual(float(total_donations), expected[TOTAL_DONOS])

    def test_03_modify_dono(self):

        number = (Donation.select(fn.MAX(Donation.dono_number)).where(
            Donation.held_by == 'New Donor').scalar()
            )

        modify_dono('New Donor', number, 2000)
        set_variables('New Donor')
        
        query = (Details.select().where(Details.name == 'New Donor'))
        query = [i for i in query][0]
        query2 = (Donation.select().where(Donation.held_by == 'New Donor'))
        dono1 = [i for i in query2][0]
        dono2 = [i for i in query2][1]
        total_donations = (Donor.select().where(Donor.donor_name == 'New Donor'))
        total_donations = [i.donations for i in total_donations][0]


        NAME = 0
        DONO_ONE = 1
        DONO_TWO = 2
        DONO_SIZE = 3
        DONO_NUMBER = 4
        TRANSACTIONS = 5
        AVERAGE = 6
        FIRST_GIFT = 7
        LAST_GIFT = 8
        TOTAL_DONOS = 9

        expected = ['New Donor', 300, 2000, 'Large', number, 2, 1150, 300, 2000, 2300]
        self.assertEqual(str(query.name), expected[NAME])
        self.assertEqual(float(dono1.dono), expected[DONO_ONE])
        self.assertEqual(float(dono2.dono), expected[DONO_TWO])
        self.assertEqual(str(dono2.dono_size), expected[DONO_SIZE])
        self.assertEqual(dono2.dono_number, expected[DONO_NUMBER])
        self.assertEqual(int(query.transactions), expected[TRANSACTIONS])
        self.assertEqual(float(query.average), expected[AVERAGE])
        self.assertEqual(float(query.first_gift), expected[FIRST_GIFT])
        self.assertEqual(float(query.last_gift), expected[LAST_GIFT])
        self.assertEqual(float(total_donations), expected[TOTAL_DONOS])
    
    def test_04_delete_dono(self):
    
        number = (Donation.select(fn.MIN(Donation.dono_number)).where(
            Donation.held_by == 'New Donor').scalar()
            )
            
        set_variables('New Donor', number)
        
        number = (Donation.select(fn.MIN(Donation.dono_number)).where(
            Donation.held_by == 'New Donor').scalar()
            )
        
        query = (Details.select().where(Details.name == 'New Donor'))
        query = [i for i in query][0]
        query2 = (Donation.select().where(Donation.held_by == 'New Donor'))
        dono1 = [i for i in query2][0]
        total_donations = (Donor.select().where(Donor.donor_name == 'New Donor'))
        total_donations = [i.donations for i in total_donations][0]

        NAME = 0
        DONO = 1
        DONO_SIZE = 2
        DONO_NUMBER = 3
        TRANSACTIONS = 4
        AVERAGE = 5
        FIRST_GIFT = 6
        LAST_GIFT = 7
        TOTAL_DONOS = 8

        expected = ['New Donor', 2000, 'Large', number, 1, 2000, 2000, 2000, 2000]
        self.assertEqual(str(query.name), expected[NAME])
        self.assertEqual(float(dono1.dono), expected[DONO])
        self.assertEqual(str(dono1.dono_size), expected[DONO_SIZE])
        self.assertEqual(dono1.dono_number, expected[DONO_NUMBER])
        self.assertEqual(int(query.transactions), expected[TRANSACTIONS])
        self.assertEqual(float(query.average), expected[AVERAGE])
        self.assertEqual(float(query.first_gift), expected[FIRST_GIFT])
        self.assertEqual(float(query.last_gift), expected[LAST_GIFT])
        self.assertEqual(float(total_donations), expected[TOTAL_DONOS])
