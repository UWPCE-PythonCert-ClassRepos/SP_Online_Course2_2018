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

        log.info('Step 2: Add customer data to the cache')
        r.hmset('Aaron', {'phone': '505-554-3729', 'zip': 11561})
        r.hmset('Blake', {'phone': '594-640-0741', 'zip': 17050})
        r.hmset('Charles', {'phone': '711-652-1354', 'zip': 16614})
        r.hmset('Denise', {'phone': '821-667-5095', 'zip': 30144})
        r.hmset('Edward', {'phone': '808-558-9987', 'zip': 46530})
        r.hmset('Frank', {'phone': '322-946-6274', 'zip': 28104})

        log.info('Step 3: Retrieve Blake\'s phone number')
        phone_blake = r.hmget('Blake', 'phone')
        log.info(f'Blake\'s phone number: {phone_blake}')

        log.info('Step 4: Retrieve Blake\'s zip code')
        zip_blake = r.hmget('Blake', 'zip')
        log.info(f'Blake\'s zip code: {zip_blake}')

    except Exception as e:
        print(f'Redis error: {e}')
