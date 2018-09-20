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
        mailroom.insert_many(get_mailroom_data())


class Donor():
    pass


def get_donor_list():
    donor_list = []
    for d in mailroom.find({}):
        donor_list.append(d['title'] + ' ' + d['last_name'])
    print(donor_list)


def query_donor_info():
    pass


def add_donor():
    pass


def update_or_remove_donor():
    pass


def get_report():
    pass


class UI():
    def __init__(self):
        # donors = Donor.select()
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
                    # database.close()
                    print('Program execution completed.')
                menu_dct[response]()

            except KeyError:
                print('\nThat selection is invalid. Please try again.')


if __name__ == '__main__':
    interaction_instance = UI()
