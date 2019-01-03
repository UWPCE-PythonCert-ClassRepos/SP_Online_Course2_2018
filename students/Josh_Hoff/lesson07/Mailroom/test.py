"""
    Unit tests for the mailroom program
"""
from .mailroom_peewee import *
from .fill_mail import populate_db, populate_donos, populate_details

from unittest import TestCase

class Mailroom_tester(TestCase):

    def setUp(self):
        populate_db()
        populate_donos()
        populate_details()
        
    def test_new_donor(self):
        #this gets the next invoice number to be used
        num = (Donation.select(fn.MAX(Donation.dono_number)).scalar())
        
        new_donor('New Donor', 300.0, 'Large', num)
            
        set_variables('New Donor')
        
        query = (Details.select().where(Details.name == 'New Donor'))
        query = [i for i in query][0]
        query2 = (Donation.select().where(Donation.held_by == 'New Donor'))
        query2 = [i for i in query2][0]
        
        NAME = 0
        DONO = 1
        DONO_SIZE = 2
        DONO_NUMBER = 3
        TRANSACTIONS = 4
        AVERAGE = 5
        FIRST_GIFT = 6
        LAST_GIFT = 7
        
        expected = ['New Donor', 300, 'Large', (num + 1), 1, 300, 300, 300]
        self.assertEqual(str(query.name), expected[NAME])
        self.assertEqual(int(query2.dono), expected[DONO])
        self.assertEqual(str(query2.dono_size), expected[DONO_SIZE])
        self.assertEqual(query2.dono_number, expected[DONO_NUMBER])
        self.assertEqual(int(query.transactions), expected[TRANSACTIONS])
        self.assertEqual(float(query.average), expected[AVERAGE])
        self.assertEqual(float(query.first_gift), expected[FIRST_GIFT])
        self.assertEqual(float(query.last_gift), expected[LAST_GIFT])
        
    def test_existing_donor(self):
        pass