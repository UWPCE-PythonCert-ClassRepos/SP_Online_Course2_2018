#!/usr/bin/env python3
import os
import datetime
import sys
from mailroom_db import Transaction
from peewee import *
import logging

logging.basicConfig(level=logging.INFO)
database = SqliteDatabase('mailroom.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')


class UserInteraction:

    def start_program(self):
        selection_dict = {'1': self.send_thank_you, '2': self.create_report,
                          '3': self.send_to_everyone, '4': self.update_row,
                          '5': self.delete_row, '6': self.quit_program}
        while True:
            selection = input('''Please enter a selection (1-4):
                               1. Send a thank you
                               2. Create a report
                               3. Send letters to everyone
                               4. Update row
                               5. Delete row
                               6. Quit
                               ''')
            try:
                selection_dict[selection]()
            except ValueError:
                print('Selection not found. Please enter a number 1-4')

    def send_thank_you(self):
        """Send a thank you note to person designated by user; add person to
        donor_info if they aren't already there"""
        while True:
            name = input('Please enter full name:\n')
            if name == 'list':
                print('This is the list of donor names:\n')
                for donor in self.get_donors():
                    print(donor.name)
            else:
                while True:
                    try:
                        donation = float(input('Please enter donation'
                                               ' amount:\n'))
                        break
                    except ValueError:
                        print('Please enter a number')

                current_donor = Donor(name)
                current_donor.add_donation(donation)
                print(current_donor.get_thank_you())
                break
        return

    def create_report(self):
        """Print summary report of donor info"""
        max_donor_width = max([len(donor_name) for donor_name in
                               self.get_donors()])
        print(self.get_report_header(max_donor_width))
        for donor_name in sorted(self.get_donors()):
            donor = Donor(donor_name)
            print(donor.get_report_row(max_donor_width))

    def get_report_header(self, max_donor_width):
        """Return string representing the header of the report"""
        return '{:{}}|{:12}|{:10}|{:8}'.format('Donor Name',
                                               max_donor_width,
                                               'Total Given',
                                               'Num Gifts',
                                               'Average Gift')

    def send_to_everyone(self, directory=os.getcwd()):
        """Write thank you notes to specified directory for each donor in
           donor_info"""
        user_dir = input('Change output directory (y/n)?')
        if user_dir.lower() == 'y':
            while True:
                directory = input('Please enter desired directory:')
                try:
                    os.chdir(directory)
                    break
                except FileNotFoundError:
                    print('Please enter a valid directory')
                except TypeError:
                    print('Please enter a valid directory')

        today = datetime.datetime.today().strftime('%Y-%m-%d')
        for donor_name in self.get_donors():
            donor = Donor(donor_name)
            filename = donor.name + '_' + today + '.txt'
            with open(filename, 'w') as f:
                print('Writing to ' + filename + '...')
                f.write(donor.get_thank_you())
            print('Finished!')


    def quit_program(self):
        """Exit program"""
        sys.exit()

    def update_row(self):
        try:
            query = (Transaction
            .select()
            .execute())
            for row in query:
                print('{:8} {:18} {:8}'.format(row.id, row.donor_name,
                                               row.donation_amount))
            idx = input('Select the index of the transaction you want '
                        'to update')
            new_value = input('Enter the new amount')
            query = (Transaction
                .update(donation_amount = new_value)
                .where(Transaction.id == idx)
                .execute())
            logging.info('Successfully updated row')
        except Exception as e:
            logging.info('Error updating row')
            logging.info(e)

    def delete_row(self):
        """I don't want to delete transactions where one user made the 
        same donation multiple times, which would occur if I deleted
        based on donor name and transaction amount. So I will give the 
        user the list of transactions and have the user delete based 
        on index"""
        try:
            query = (Transaction
            .select()
            .execute())
            for row in query:
                print('{:8} {:18} {:8}'.format(row.id, row.donor_name,
                                               row.donation_amount))
            idx = input('Select the index of the transaction you want'
                        ' to delete')
            query = (Transaction
                .delete()
                .where(Transaction.id == idx)
                .execute())
            logging.info('Successfully deleted row')
        except Exception as e:
            logging.info('Error deleting row')
            logging.info(e)

    def get_donors(self):
        try:
            query = (Transaction
                .select(Transaction.donor_name).distinct())
            return [i.donor_name for i in query]
        except Exception as e:
            logging.info('Failed to retrieve donor names')
            logging.info(e)


class Donor:
    def __init__(self, name):
        self.name = name

    def add_donation(self, donation):
        try:
            with database.transaction():
                new_donation = Transaction.create(
                    donor_name = self.name,
                    donation_amount = donation
                    )
                new_donation.save()
                logging.info('Added donation')
        except Exception as e:
            logging.info('Error adding donation to database')
            logging.info(e)

    def get_average_donation(self):
        try:
            query = (Transaction
                .select(Transaction.donation_amount)
                .where(Transaction.donor_name == self.name))
            return float(sum([i.donation_amount for i in query])
                         / len(query))
        except Exception as e:
            logging.info('Error calculating average donation')
            logging.info(e)

    def get_num_donations(self):
        try:
            query = (Transaction
                .select(Transaction.donation_amount)
                .where(Transaction.donor_name == self.name))
            return len(query)
        except Exception as e:
            logging.info('Error calculating number of donations')
            logging.info(e)

    def get_most_recent_donation(self):
        try:
            query = (Transaction
                .select()
                .order_by(Transaction.id.desc()))
            return list(query)[0].donation_amount
        except Exception as e:
            logging.info('Error retrieving most recent donation')
            logging.info(e)

    def get_sum_donations(self):
        try:
            query = (Transaction
                .select(Transaction.donation_amount)
                .where(Transaction.donor_name == self.name))
            return float(sum([i.donation_amount for i in query]))
        except Exception as e:
            logging.info('Error calculating sum of donations')
            logging.info(e)

    def get_thank_you(self):
        number_donations = self.get_num_donations()
        donor_dict = {'name': self.name, 'donation':
                       self.get_most_recent_donation(),
                      'num_donations': number_donations}
        donor_dict['multiple'] = 's' if number_donations > 1 else ''

        thankyou = ('Dear {name}:\n'
                    'Thank you for your generous donation of '
                    '${donation:.2f}.\nI really appreciate your '
                    '{num_donations}\ndonation{multiple} to our '
                    'organization.\nI assure you that your contributions '
                    'will be put to\ngood use!\n\n'
                    'Regards,\nBen').format(**donor_dict)

        return thankyou

    def get_report_row(self, max_donor_width):
        """Return string representing one row in report"""
        return '{:{}}|${:^11.2f}|{:^10}|${:^8.2f}'.format(self.name,
                                                      max_donor_width,
                                                      self.get_sum_donations(),
                                                      self.get_num_donations(),
                                                      self.get_average_donation())

    def __lt__(self, other):
        return self.get_sum_donations() > other.get_sum_donations()


def main():
    ui = UserInteraction()
    ui.start_program()

if __name__ == '__main__':
    main()