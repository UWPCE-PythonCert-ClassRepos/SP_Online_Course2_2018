"""
    Creates redis database for mailroom
"""

import sys
from random import choice as rc
from login_database import login_redis_cloud

r = login_redis_cloud()
r.flushdb()


def create_random_phone():
    area = rc(['206-', '360-', '425-'])
    prefix = rc(['234-', '321-', '456-', '987-'])
    suffix = rc(['1212', '2789', '3767', '4123', '5555'])
    return area + prefix + suffix


def create_random_email():
    donor_suffix = rc(['3000', '5000', '7000'])
    domain = rc(['@gmail.com', '@hotmail.com', '@outlook.com'])
    return donor_suffix + domain


def choose_random_zip():
    return rc(['98101', '98112', '98127', '98155'])


def cache_data():
    """
        given redis's non-robust querying, donor data is hardcoded here
    """
    r.hmset('donor:Gates', {'title': 'Mr.', 'donations': 150000,
                            'num_donations': 3,
                            'phone': create_random_phone(),
                            'email': 'gates' + create_random_email(),
                            'zip': choose_random_zip()})
    r.hmset('donor:Brin', {'title': 'Mr.', 'donations': 150000,
                           'num_donations': 3,
                           'phone': create_random_phone(),
                           'email': 'brin' + create_random_email(),
                           'zip': choose_random_zip()})
    r.hmset('donor:Cerf', {'title': 'Mr.', 'donations': 50000,
                           'num_donations': 2,
                           'phone': create_random_phone(),
                           'email': 'cerf' + create_random_email(),
                           'zip': choose_random_zip()})
    r.hmset('donor:Musk', {'title': 'Mr.', 'donations': 100000,
                           'num_donations': 1,
                           'phone': create_random_phone(),
                           'email': 'musk' + create_random_email(),
                           'zip': choose_random_zip()})
    r.hmset('donor:Berners-Lee', {'title': 'Mr.', 'donations': 50000,
                                  'num_donations': 2,
                                  'phone': create_random_phone(),
                                  'email': 'tbl' + create_random_email(),
                                  'zip': choose_random_zip()})
    r.hmset('donor:Wojcicki', {'title': 'Ms.', 'donations': 125000,
                               'num_donations': 1,
                               'phone': create_random_phone(),
                               'email': 'awoj' + create_random_email(),
                               'zip': choose_random_zip()})
    r.hmset('donor:Avey', {'title': 'Ms.', 'donations': 200000,
                           'num_donations': 2,
                           'phone': create_random_phone(),
                           'email': 'avey' + create_random_email(),
                           'zip': choose_random_zip()})


def get_one_donor_data():
    """
        simple query to cache for one donor's data
    """
    while True:
        q_last_name = input('Enter donor\'s last name, or "e" to exit: ')
        if q_last_name.lower() == 'e':
            break
        else:
            donor = 'donor:' + q_last_name
            print(r.hmget(donor, 'title', 'donations', 'num_donations',
                          'phone', 'email', 'zip'))
            # print('title:', r.hget(donor, 'title'))
            # print('total donations:', r.hget(donor, 'donations'))
            # print('number of donations:', r.hget(donor, 'num_donations'))


def get_donor_list():
    """
        returns list of all donor keys
    """
    print(r.keys())


class UI():
    def __init__(self):
        menu_dct = {
            '1': get_donor_list,
            '2': get_one_donor_data,
            'q': sys.exit
            }
        main_text = '\n'.join((
            'Choose from the following:',
            '"1" - Get a List of Donors,',
            '"2" - Get Data from All Fields for One Donor, or',
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
    cache_data()
    interaction_instance = UI()
