"""
    Creates redis database for mailroom
"""

import sys
from login_database import login_redis_cloud
from learn_data import get_mailroom_data


r = login_redis_cloud()


def make_cache_dict():
    cache_dict = {}
    for d_dict in get_mailroom_data():
        d_key = 'donor:' + d_dict['last_name']
        try:
            cache_dict[d_key] = {k: v for k, v in d_dict.items() if
                                 k != 'last_name'}
        except Exception as e:
            print(f'Error occurred at {e}')
    return cache_dict


def make_hmset_statements():
    hmset_statements_list = []
    for donor, d_dict in make_cache_dict().items():
        r_string = "r.hmset('" + donor + "', " + str(d_dict) + ")"
        hmset_statements_list.append(r_string)
    # for s in hmset_statements_list:
    #     print(s)
    return hmset_statements_list


def run_hmset_statements():
    for s in make_hmset_statements():
        s = s.strip('"')
        print(s)


def make_hmget_statements():
    hmget_statements_list = []
    for donor, d_dict in make_cache_dict().items():
        r_string = "r.hmget('" + donor + "', " + str(d_dict) + ")"
        hmget_statements_list.append(r_string)
    return hmget_statements_list


def get_donor_list():
    # donor_list = []
    for s in make_hmget_statements():
        donor = s.strip('"')
        print(donor)
    # return [s.strip('"') for s in make_hmget_statements()]
    # print(donor_list)


class UI():
    def __init__(self):
        menu_dct = {
            '1': get_donor_list,
            # '2': get_report,
            # '3': add_donor,
            # '4': update_or_remove_donor,
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
    run_hmset_statements()
    interaction_instance = UI()
