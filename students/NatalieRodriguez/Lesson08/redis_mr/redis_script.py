"""
    Redis
"""

import login_db
import utilities


def run_example():
    """
        non-presistent Redis
    """

    log = utilities.configure_logger('default', '../logs/redis_script.log')

    try:
        log.info('Step 1: connect to Redis.')
        r = login_db.login_redis_cloud()

        log.info('Step 2: Add donor data to cache.')
        r.hmset('Luke Rodriguez', {'phone': '319-706-8805', 'zip': 60012,
                          'donation': [45, 76, 100], 'email': 'lukerod@gmail.com'})
        r.hmset('Virgil Ferdinand', {'phone': '913-366-2202', 'zip': 75019,
                          'donation': [3500, 50], 'email': 'virgilia@outlook.com'})
        r.hmset('River Tails', {'phone': '972-310-1058', 'zip': 61761,
                            'donation': [4000], 'email': 'river.tails@gmail.com'})
        r.hmset('Joseph Kibson', {'phone': '309-304-0112', 'zip': 61704,
                           'donation': [12, 25, 350, 450], 'email': 'joekib@yahoo.com'})
        r.hmset('Emily Connor', {'phone': '387-696-2058', 'zip': 43055,
                           'donation': [20], 'email': 'emmyc416@msn.com'})

    except Exception as e:
        print(f'Redis error: {e}')


def donor_input():
    return input("Enter a donor name or enter 'List'" +
                 " for a list of donors.\n>")


def donation_prompt():
    return input("Enter a donation amount: \n>")


def list_donors():
    try:
        r = login_db.login_redis_cloud()
        for i in r.keys():
            print(i)
    except Exception as e:
        print(f'Redis error: {e}')


def send_thankyou():
    don_input = None
    while not don_input:
        don_input = donor_input()
        if don_input.lower() == "list":
            list_donors()
            don_input = None

    donation = None
    while not donation:
        try:
            donation = int(donation_prompt())
        except ValueError:
            print("Enter a monetary donation.")
    phone = input('Enter phone number (nnn-nnn-nnnn: ')
    zip = input('Enter zip code (nnnnn): ')
    email = input('Enter email address: ')
    try:
        r = login_db.login_redis_cloud()
        r.hmset(don_input, {'phone': phone,
                            'zip': zip,
                            'donation': [donation],
                            'email': email})
    except:
        print("There was an error adding donor to database.")

    print("Thank you {} for your donation of ${}."
          .format(don_input, donation))


def send_thankyou_total(donor, donation):
    return ("Dear {}, \n We are thankful for your donation of ${}. ".format(donor, donation) +
            "We are extremely grateful for your dedication to the protection and " +
            "preservation of the environment. " +
            "Sincerely, " +
            "The Nature Conservancy")


def create_report():
    print('{:20} | {:20} | {:20} | {:20}'.format(
        'Donor Name', 'Donations', 'Phone No.', 'Email'))
    print('-' * 80)
    try:
        r = login_db.login_redis_cloud()
        for i in r.keys():
            print('{:20} | {:20} | {:20} | {:20}'.format(
                i, r.hget(i, 'donation'),
                r.hget(i, 'phone'),
                r.hget(i, 'email')))
    except Exception as e:
        print(f'Redis error: {e}')


def send_letters():
    r = login_db.login_redis_cloud()
    for i in r.keys():
        with open('{}.txt'.format(i), 'w') as donorfh:
            donorfh.write(send_thankyou_total(i, r.hget(i, 'donation')))


def close_program():
    print('\nClosing Program.\n')


def lookup_email():
    donor = input('Enter Donor Name to find their email address.\n')
    try:
        r = login_db.login_redis_cloud()
        if r.exists(donor):
            print('{}\'s email is: {}'.format(donor, r.hget(donor, 'email')))
        else:
            print('{} is not in the database.'.format(donor))
    except Exception as e:
        print(f'Redis error: {e}')


def delete_donor():
    name = input('Enter name to delete from database: ')
    r = login_db.login_redis_cloud()
    if r.exists(name):
        r.delete(name)
    else:
        print('{} is not in the database.'.format(name))