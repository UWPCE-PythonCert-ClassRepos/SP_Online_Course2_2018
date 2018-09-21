"""
    Creates mongodb database for mailroom
"""

from learn_data import get_mailroom_data
import login_database
import pprint
import sys
import utilities

log = utilities.configure_logger('default', '../logs/mailroom_mdb.log')

with login_database.login_mongodb_cloud() as client:
        db = client['dev']
        mailroom = db['mailroom']
        # mailroom.insert_many(get_mailroom_data()) -- used for 1st init


class Donor():
    pass


def get_donor_list():
    donor_list = []
    for d in mailroom.find({}):
        donor_list.append(d['title'] + ' ' + d['last_name'])
    print(donor_list)


def query_donor_info():
    title = input('Enter donor title: ')
    last_name = input('Enter last name: ')
    total_donation_amt = int(input('Enter total donation amount: '))
    num_donations = int(input('Enter number of donations: '))
    query_dict = {'title': title, 'last_name': last_name,
                  'total_donation_amt': total_donation_amt,
                  'num_donations': num_donations}
    return query_dict


def add_donor(*donor):
    if donor:
        updated_donor = mailroom.insert(donor)
        print(updated_donor['title'], updated_donor['last_name'], 'updated')
    else:
        new_donor = query_donor_info()
        new_donor = mailroom.insert(new_donor)
        print(new_donor.title, new_donor.lastname, 'added to database')


def update_or_remove_donor():
    pass


def get_report():
    pass


class UI():
    def __init__(self):
        menu_dct = {'1': get_donor_list,
                    '2': get_report,
                    '3': add_donor,
                    '4': update_or_remove_donor,
                    'q': sys.exit}
        main_text = '\n'.join((
                               'Choose from the following:',
                               '"1" - Get a List of Donors,',
                               '"2" - Create a Report,',
                               '"3" - Add a Donor,',
                               '"4" - Update or Remove a Donor, or',
                               '"q" to Quit: '
                               ))
        while True:
            print('\nMain Menu:')
            response = input(main_text)
            print()
            try:
                if response.lower() == 'q':
                    print('Program execution completed.')
                menu_dct[response]()

            except KeyError:
                print('\nThat selection is invalid. Please try again.')


if __name__ == '__main__':
    interaction_instance = UI()
