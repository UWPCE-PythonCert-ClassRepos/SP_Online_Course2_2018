from unittest import TestCase
from unittest.mock import MagicMock, call
from unittest.mock import patch

# import unittest
# unittest.util._MAX_LENGTH = 500

from decimal import Decimal

import io
import os
import sys

from populate_mailroom_db import populate_db
from mailroom import *


# Test database (Delete it if it already exists)
try:
    os.remove('test.db')
except FileNotFoundError:
    pass

database.init('test.db', pragmas={'foreign_keys': 1})
database.connect()
database.create_tables([Donor, Donation])
database.close()

donors = [
    ('bob', '2013-11-11', [(3468.34, '2013-11-14')]),
    ('joe', '2017-06-01', [(5286286.3, '2019-03-21'), (567.5879, '2019-03-24'), (23, '2017-07-06')]),
    ('becky sue', '2011-01-01', [(432, '2011-09-06'), (679.4553, '2013-05-24')])
    ]
populate_db('test.db', donors)


class AddOrGetTests(TestCase):

    def setUp(self):
        self.mailroom = Mailroom('test.db')
        self.mailroom.add_donor = MagicMock()
        self.mailroom.add_donation = MagicMock()
        self.mailroom.thank = MagicMock()

    @patch('builtins.print', MagicMock())
    def test_add_or_get(self):
        self.mailroom.input_donor_name = MagicMock(return_value='bob')
        self.mailroom.input_donation_amount = MagicMock(return_value=56.7)

        self.mailroom.add_or_get_donor_add_donation()

        self.mailroom.add_donor.assert_called_with('bob')
        self.mailroom.add_donation.assert_called_with('bob', 56.7)
        self.mailroom.thank.assert_called_with('bob', 56.7)

    def test_add_or_get_add_donor_exception(self):
        self.mailroom.input_donor_name = MagicMock(side_effect=MainMenu())
        self.mailroom.input_donation_amount = MagicMock(return_value=56.7)

        self.mailroom.add_or_get_donor_add_donation()

        self.mailroom.add_donor.assert_not_called()
        self.mailroom.input_donation_amount.assert_not_called()
        self.mailroom.add_donation.assert_not_called()
        self.mailroom.thank.assert_not_called()

    def test_add_or_get_add_donation_exception(self):
        self.mailroom.input_donor_name = MagicMock(return_value='bob')
        self.mailroom.input_donation_amount = MagicMock(side_effect=MainMenu())

        self.mailroom.add_or_get_donor_add_donation()

        self.mailroom.add_donor.assert_called_with('bob')
        self.mailroom.add_donation.assert_not_called()
        self.mailroom.thank.assert_not_called()


class CreateReportTests(TestCase):

    def setUp(self):
        self.mailroom = Mailroom('test.db')

    def test_create_report(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.mailroom.create_report()
        sys.stdout = sys.__stdout__
        self.assertEqual(
            captured_output.getvalue(),
            'Donor Name |  Total Given  | Num Gifts |  Average Gift \n' +
            'joe        | $  5286876.89 |         3 | $   1762292.30\n' +
            'bob        | $     3468.34 |         1 | $      3468.34\n' +
            'becky sue  | $     1111.46 |         2 | $       555.73\n'
        )


class SendLettersTests(TestCase):

    output_test = MagicMock()
    output_test.write = MagicMock()
    open_mock = MagicMock(return_value=output_test)

    def setUp(self):
        self.mailroom = Mailroom('test.db')
        self.mailroom.thank = MagicMock()

    @patch('builtins.open', open_mock)
    def test_send_letters(self):
        date = datetime.date.today()

        self.mailroom.send_letters()
        self.assertEqual(self.open_mock.mock_calls, [
            call(f'bob_{date.month}_{date.day}_{date.year}.txt', 'w'),
            call(f'joe_{date.month}_{date.day}_{date.year}.txt', 'w'),
            call(f'becky_sue_{date.month}_{date.day}_{date.year}.txt', 'w')
            ])

        self.assertEqual(self.mailroom.thank.mock_calls, [
            call('bob', Decimal('3468.34')),
            call('joe', Decimal('567.59')),
            call('becky sue', Decimal('679.46'))
            ])


class DeleteDonorTests(TestCase):

    def setUp(self):
        self.mailroom = Mailroom('test.db')
        self.mailroom.delete_from_db = MagicMock()

    def test_delete_donor(self):
        self.mailroom.input_donor_name = MagicMock(return_value='bob')
        self.mailroom.delete_donor()
        self.mailroom.delete_from_db.assert_called_with('bob')

    def test_delete_donor_exception(self):
        self.mailroom.input_donor_name = MagicMock(side_effect=MainMenu)
        self.mailroom.delete_donor()
        self.mailroom.delete_from_db.assert_not_called()


class QuitTests(TestCase):

    def setUp(self):
        self.mailroom = Mailroom('test.db')

    def test_quit(self):
        self.mailroom.database = MagicMock()
        self.mailroom.database.close = MagicMock()

        with self.assertRaises(ExitScript):
            self.mailroom.quit()
            self.mailroom.database.close.assert_called_once()


class InputDonorNameTests(TestCase):

    def setUp(self):
        self.mailroom = Mailroom('test.db')

    @patch('builtins.input', MagicMock(return_value='bob'))
    def test_name_input(self):
        self.assertEqual(self.mailroom.input_donor_name(), 'bob')

    @patch('builtins.input', MagicMock(return_value='return'))
    def test_return(self):
        with self.assertRaises(MainMenu):
            self.mailroom.input_donor_name()


class InputDonationAmountTests(TestCase):

    def setUp(self):
        self.mailroom = Mailroom('test.db')

    @patch('builtins.input', MagicMock(return_value=55.4))
    def test_amount_input(self):
        self.assertEqual(self.mailroom.input_donation_amount(), 55.4)

    @patch('builtins.input', MagicMock(return_value='return'))
    def test_return(self):
        with self.assertRaises(MainMenu):
            self.mailroom.input_donation_amount()


class ListDonorsTests(TestCase):

    def setUp(self):
        self.mailroom = Mailroom('test.db')

    def test_list_donors(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.mailroom.list_donors()
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue(), 'becky sue\nbob\njoe\n')


class AddDonorTests(TestCase):

    def setUp(self):
        self.mailroom = Mailroom('test.db')

    def test_add_new_donor(self):
        with database.transaction():
            captured_output = io.StringIO()
            sys.stdout = captured_output
            self.mailroom.add_donor('fred')
            sys.stdout = sys.__stdout__
            self.assertEqual(captured_output.getvalue(),
                                'Donor not in database. Adding donor.\n')
            self.assertIn('fred', (donor.name for donor in Donor.select()))

            self.mailroom.delete_from_db('fred')

    def test_add_existing_donor(self):
        with database.transaction():
            new_donor = Donor.create(name='fred', date_added=datetime.date.today())
            new_donor.save()
            captured_output = io.StringIO()
            sys.stdout = captured_output
            self.mailroom.add_donor('fred')
            sys.stdout = sys.__stdout__
            self.assertEqual(captured_output.getvalue(),
                              'This donor already exists. Adding a new donation...\n')
            self.mailroom.delete_from_db('fred')


class AddDonationTests(TestCase):

    def setUp(self):
        self.mailroom = Mailroom('test.db')

    def test_add_donation(self):
        with database.transaction():
            new_donor = Donor.create(name='fred', date_added=datetime.date.today())
            new_donor.save()
            self.mailroom.add_donation('fred', 78.9812)
            Donation.get(Donation.amount == 78.98)
            self.mailroom.delete_from_db('fred')

    def test_add_donation_nonexistant_donor(self):
        with self.assertRaises(IntegrityError):
            self.mailroom.add_donation('billy bob', 56)


class DeleteFromDbTests(TestCase):

    def setUp(self):
        self.mailroom = Mailroom('test.db')

    def test_delete_from_db(self):
        with database.transaction():
            new_donor = Donor.create(name='fred', date_added=datetime.date.today())
            new_donor.save()
            self.mailroom.delete_from_db('fred')
            self.assertNotIn('fred', (donor.name for donor in Donor.select()))

    def test_delete_from_db_nonexistant_donor(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.mailroom.delete_from_db('betsy')
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue(),
                         "This donor doesn't exist.\n")


class ThankTest(TestCase):

    def setUp(self):
        self.mailroom = Mailroom('test.db')

    def test_thank(self):
        self.assertEqual(
            self.mailroom.thank('joe', 23),
            "Dear joe,\n\n" +
            "Thank you so much for your generous donation of $23.00.\n\n" +
            "We really appreciate your donations totalling $5286876.89.\n" +
            "Sincerely, The Wookie Foundation"
            )


class SizeReportTests(TestCase):

    def setUp(self):
        self.mailroom = Mailroom('test.db')

    def test_size_report(self):
        donors = (Donor.select())
        self.assertEqual(self.mailroom.size_report(donors), [10, 11, 9, 12])
