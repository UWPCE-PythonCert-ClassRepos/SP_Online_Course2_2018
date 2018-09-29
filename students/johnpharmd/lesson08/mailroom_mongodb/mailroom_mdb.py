"""
    Creates mongodb database for mailroom
"""

import sys
# from learn_data import get_mailroom_data
import login_database
import utilities

log = utilities.configure_logger('default', '../logs/mailroom_mdb.log')

with login_database.login_mongodb_cloud() as client:
    db = client['dev']
    mailroom = db['mailroom']
    # mailroom.insert_many(get_mailroom_data()) -- used for 1st init


def get_donor_list():
    donor_list = []
    for d in mailroom.find():
        donor_list.append(d['title'] + ' ' + d['last_name'])
    print(donor_list)


def query_donor_info():
    title = input('Enter donor title: ')
    last_name = input('Enter last name: ')
    donations = int(input('Enter total donation amount: '))
    num_donations = int(input('Enter number of donations: '))
    query_dict = {'title': title, 'last_name': last_name,
                  'donations': donations,
                  'num_donations': num_donations}
    return query_dict


def add_donor(**donor):
    if donor:
        print(donor['title'], donor['last_name'], 'updated')
        mailroom.insert_one(donor)
    else:
        new_donor = query_donor_info()
        print(new_donor['title'], new_donor['last_name'], 'added to database')
        mailroom.insert_one(new_donor)


def update_or_remove_donor():
    q_title = input('Enter donor title: ')
    q_lastname = input('Enter last name: ')
    query = {}
    for ddoc in mailroom.find():
        if ddoc['title'] == q_title and ddoc['last_name'] == q_lastname:
            query = ddoc
    mailroom.delete_one(query)
    response = input('[U]pdate or [r]emove this donor? ')
    if response.lower() == 'u':
        print('Re-enter values for each of the donor\'s fields')
        updated_donor = query_donor_info()
        add_donor(**updated_donor)
    elif response.lower() == 'r':
        print(query['title'], query['last_name'], 'removed from database')


def get_report():
    print()
    psv = ['Donor Name', '| Total Given', '| Num Gifts',
           '| Average Gift']
    print('{:<15}{:>12}{:>12}{:>12}'.format(psv[0], psv[1],
                                            psv[2], psv[3]))
    for i in range(55):
        print('-', end='')
    print()
    new_list = []
    try:
        for ddoc in mailroom.find():
            new_list.append([ddoc['donations'], ddoc['last_name'],
                             ddoc['num_donations']])
    except Exception as e:
        print(f'Error in for loop, and {e}')

    new_list.sort(reverse=True)
    for d_list in new_list:
        formatted_donor = ('{:<15}'.format(d_list[1])
                           + '{}{:>10}'.format(' $', d_list[0])
                           + '{:>13}'.format(d_list[2])
                           + '{}{:>11}'.format(' $',
                                               d_list[0] // d_list[2]))
        print(formatted_donor)


class UI():
    def __init__(self):
        menu_dct = {
            '1': get_donor_list,
            '2': get_report,
            '3': add_donor,
            '4': update_or_remove_donor,
            'q': sys.exit
            }
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
