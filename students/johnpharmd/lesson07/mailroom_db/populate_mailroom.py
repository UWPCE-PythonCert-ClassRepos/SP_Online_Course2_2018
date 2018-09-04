from peewee import *
from datetime import *
import sys


database = SqliteDatabase('mailroom.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')


class BaseModel(Model):
    class Meta:
        database = database


class Donor(BaseModel):
    """
        This class defines Donor instances, each of which maintains
        details of an individual donor.
    """
    title = CharField(max_length=10)
    last_name = CharField(primary_key=True, max_length=30)
    total_donation_amt = IntegerField()
    num_donations = IntegerField()


def get_donor_list():
    print([donor.last_name for donor in Donor])


def add_or_remove_donor():
    response = input('[A]dd or [r]emove donor? ')
    q_title = input('Enter donor title: ')
    q_lastname = input('Enter last name: ')
    if response.lower() == 'a':
        q_donation = int(input('Donation amount (USD)?: '))
        with database.transaction():
            new_donor = Donor.create(
                    title=q_title,
                    last_name=q_lastname,
                    total_donation_amt=q_donation,
                    num_donations=1)
            new_donor.save()
            print(q_title, q_lastname, 'added as a Donor')
    elif response.lower() == 'r':
        for donor in Donor:
            if donor.title == q_title and donor.last_name == q_lastname:
                print(q_title, q_lastname, 'removed from Donors')
                donor.delete_instance()


def update_donor():
    pass


def get_donorgroup_report():
    pass


def get_report(self):
    print()
    psv = ['Donor Name', '| Total Given', '| Num Gifts',
           '| Average Gift']
    print('{:<15}{:>12}{:>12}{:>12}'.format(psv[0], psv[1],
          psv[2], psv[3]))
    for i in range(55):
        print('-', end='')
    print()
    new_list = []
    for donor in self.donors:
        new_list.append([self.donors[donor]['donations'], donor,
                        self.donors[donor]['num_donations']])
    new_list.sort(reverse=True)
    for donor_list in new_list:
        formatted_donor = ('{:<15}'.format(donor_list[1])
                           + '{}{:>10}'.format(' $', donor_list[0])
                           + '{:>13}'.format(donor_list[2])
                           + '{}{:>11}'.format(' $',
                           donor_list[0] // donor_list[2]))
        print(formatted_donor)


class UI():
    def __init__(self):
        database.create_tables([Donor])
        donors = Donor.select()
        self.menu_dct = {'1': get_donor_list,
                         '2': get_report,
                         '3': add_or_remove_donor,
                         '4': update_donor,
                         'q': sys.exit}
        self.main_text = '\n'.join((
                                    'Choose from the following:',
                                    '"1" - Get a List of Donors,',
                                    '"2" - Create a Report,',
                                    '"3" - Add or Remove a Donor,',
                                    '"4" - Update a Donor, or',
                                    '"q" to Quit: '
                                  ))
        while True:
            print('\nMain Menu:')
            response = input(self.main_text)
            print()
            try:
                if response == 'q':
                    database.close()
                    print('Program execution completed.')
                if type(self.menu_dct[response]) != list:
                    self.menu_dct[response]()
                else:
                    print(self.menu_dct[response])

            except KeyError:
                print('\nThat selection is invalid. Please try again.')


interaction_instance = UI()
