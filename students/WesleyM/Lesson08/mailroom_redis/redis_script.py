"""
    demonstrate use of Redis
"""


import login_database
import utilities


def run_example():
    """
        uses non-presistent Redis only (as a cache)

    """

    log = utilities.configure_logger('default', '../logs/redis_script.log')

    try:
        log.info('Step 1: connect to Redis')
        r = login_database.login_redis_cloud()

        log.info('Step 2: Add donor data to the cache')
        r.hmset('Aaron', {'phone': '505-554-3729', 'zip': 11561,
                          'donation': [20], 'email': 'aaron@gmail.com'})
        r.hmset('Blake', {'phone': '594-640-0741', 'zip': 17050,
                          'donation': [20, 50], 'email': 'blake@gmail.com'})
        r.hmset('Charles', {'phone': '711-652-1354', 'zip': 16614,
                            'donation': [100], 'email': 'boyle@gmail.com'})
        r.hmset('Denise', {'phone': '821-667-5095', 'zip': 30144,
                           'donation': [5], 'email': 'dnice@gmail.com'})
        r.hmset('Edward', {'phone': '808-558-9987', 'zip': 46530,
                           'donation': [15], 'email': 'ededed@gmail.com'})

    except Exception as e:
        print(f'Redis error: {e}')

def donor_input():
        return input("Enter a donor name or input 'List'"+
                     " for a list of donors\n>")

def donation_prompt():
    return input("Enter a donation amount \n>")

def list_donors():
    try:
        r = login_database.login_redis_cloud()
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
            print("Enter donations numerically")
    phone = input('Input phone number in format XXX-XXX-XXXX: ')
    zpcd = input('Input zip code in format: XXXXX: ')
    email = input('Input email address: ')
    try:
        r = login_database.login_redis_cloud()
        r.hmset(don_input, {'phone': phone,
                            'zip': zpcd,
                            'donation': [donation],
                            'email': email})
    except:
        print("Error in inputing user to database")
    
    print("Thank you {} for your donation of ${}"
              .format(don_input, donation))

def send_thankyou_total(donor, donation):
    return ("Dear Ms./Mrs./Mr./Dr. {}, \n We are thankful for your donation(s) of ${}. ".format(donor, donation) +
            "Your donation will be used for (insert harmful activity here). " +
            "We hope you donate again soon!")

def create_report():
    print('{:20} | {:20} | {:20} | {:20}'.format(
        'Donor Name', 'Donations', 'Phone', 'Email'))
    print('-'*80)
    try:
        r = login_database.login_redis_cloud()
        for i in r.keys():
            print('{:20} | {:20} | {:20} | {:20}'.format(
                i, r.hget(i, 'donation'),
                r.hget(i, 'phone'),
                r.hget(i, 'email')))
    except Exception as e:
        print(f'Redis error: {e}')

def send_letters():
    r = login_database.login_redis_cloud()
    for i in r.keys():
        with open('{}.txt'.format(i), 'w') as donorfh:
            donorfh.write(send_thankyou_total(i, r.hget(i, 'donation')))

def close_program():
    print('\nClosing Program\n')

def lookup_email():
    donor = input('Enter Donor Name to Search for Email\n')
    try:
        r = login_database.login_redis_cloud()
        if r.exists(donor):
            print('{}\'s email is: {}'.format(donor, r.hget(donor, 'email')))
        else:
            print('{} is not in the database'.format(donor))
    except Exception as e:
        print(f'Redis error: {e}')

def delete_donor():
    name = input('Enter name to delete from database: ')
    r = login_database.login_redis_cloud()
    if r.exists(name):
        r.delete(name)
    else:
        print('{} is not in the database'.format(name))
