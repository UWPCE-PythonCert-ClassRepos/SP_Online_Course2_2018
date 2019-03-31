"""
Demonstrate use of Redis
"""


import login_database
import utilities


def run_example():
    """
        uses non-presistent Redis only (as a cache)
    """

    log = utilities.configure_logger('default', '../logs/redis_script.log')

    try:
        log.info('Step 1: Connect to Redis')
        r = login_database.login_redis_cloud()

        log.info('Step 2: Adding 8 customers to the data cache')
        r.hmset('Bill', {'phone': '2538-234-1433', 'zip': 98277})
        r.hmset('Elon', {'phone': '125-290-2443', 'zip': 23904})
        r.hmset('Jeff', {'phone': '654-490-2300', 'zip': 49039})
        r.hmset('Nikola', {'phone': '453-872-9982', 'zip': 23922})
        r.hmset('Steve', {'phone': '238-403-4923', 'zip': 34095})
        r.hmset('John', {'phone': '299-343-4785', 'zip': 18492})
        r.hmset('Joe', {'phone': '947-239-1114', 'zip': 24909})
        r.hmset('Harry', {'phone': '808-333-9942', 'zip': 54848})

        log.info('Step 3: Retrieve zip code')
        ret_zip = r.hmget('Elon', 'zip')
        log.info(f"Elon's zip is {ret_zip[0]}.")

        log.info('Step 4: Retrieve phone number')
        ret_phone = r.hmget('John', 'phone')
        log.info(f"John's phone number is {ret_phone[0]}.")

    except Exception as e:
        print(f'Redis error: {e}')


if __name__ == '__main__':
    run_example()
