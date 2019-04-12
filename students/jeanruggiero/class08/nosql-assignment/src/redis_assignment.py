"""
    demonstrate use of Redis
"""


import login_database
import utilities


def add_customers():
    """
        uses non-presistent Redis only (as a cache)

    """

    PHONE = 0
    ZIP = 1

    customers = {
        'joe': {
            'phone': '9086543218',
            'zip': '86902'
        },
        'bob': {
            'phone': '8976543456',
            'zip': '93675'
        },
        'fred': {
            'phone': '7356497673',
            'zip': '84720'
        },
        'sue': {
            'phone': '1847264092',
            'zip': '09164'
        },
        'mary': {
            'phone': '8642876530',
            'zip': '92810'
        },
        'james': {
            'phone': '8503926593',
            'zip': '02958'
        }
    }

    log = utilities.configure_logger('default', '../logs/redis_script.log')

    try:
        log.info('Step 1: connect to Redis')
        r = login_database.login_redis_cloud()

        log.info('Step 2: cache customer data in Redis')
        for customer, data in customers.items():
            r.set(customer+'_phone', data['phone'])
            r.set(customer+'_zip', data['zip'])

        log.info("Step 3: Retrieve Joe's phone number.")
        phone = r.get('joe_phone')
        log.info(f"Joe's phone number is: {phone}.")

        log.info("Step 4: Retrieve Joe's zip code.")
        zipcode = r.get('joe_zip')
        log.info(f"Joe's zip code is: {zipcode}.")

    except Exception as e:
        print(f'Redis error: {e}')
        raise e
