"""
    store donor zip codes in redis 
"""


import login_database
import utilities


def set_donor_zip_code(donor_name, zip_code):

    log = utilities.configure_logger('default', '../logs/redis_script.log')

    try:
        r = login_database.login_redis_cloud()
        r.set(donor_name, zip_code)

        email = r.get('andy')

    except Exception as e:
        print(f'Redis error: {e}')

def get_donor_zip_code(donor_name):

    log = utilities.configure_logger('default', '../logs/redis_script.log')

    zip_code = ''
    try:
        r = login_database.login_redis_cloud()
        zip_code = r.get(donor_name)

    except Exception as e:
        print(f'Redis error: {e}')

    return zip_code
