"""
    demonstrate use of Redis
"""


import login_database
import utilities


def run_example():
    """
        uses non-presistent Redis only (as a cache)

    """

    log = utilities.configure_logger('default', 'logs/redis_script.log')

    try:
        log.info('Step 1: connect to Redis')
        r = login_database.login_redis_cloud()
        log.info('Step 2: cache some data in Redis')
        r.set('andy', 'andy@somewhere.com')

        log.info('Step 2: now I can read it')
        email = r.get('andy')
        log.info('But I must know the key')
        log.info(f'The results of r.get: {email}')

        log.info('Step 3: cache more data in Redis')
        r.set('pam', 'pam@anywhere.com')
        r.set('fred', 'fred@fearless.com')

        telephone = 0
        zip_code = 1

        r.rpush('Alex', 2067771111)
        r.rpush('Alex', 98144)

        r.rpush('Reid', 2065551212)
        r.rpush('Reid', 98122)

        r.rpush('Ben', 2067896666)
        r.rpush('Ben', 98104)

        r.rpush('Tom', 2064561298)
        r.rpush('Tom', 98139)

        r.rpush('Hannah', 2069876543)
        r.rpush('Hannah', 98106)

        r.rpush('Ezra', 2061234567)
        r.rpush('Ezra', 98120)

        e_phone = r.lindex('Ezra', telephone)
        log.info(f'Ezra Phone Number = {e_phone}')
        e_zip = r.lindex('Ezra', zip_code)
        log.info(f'Ezra Zip Code = {e_zip}')

        '''
        log.info('Step 4: delete from cache')
        r.delete('andy')
        log.info(f'r.delete means andy is now: {email}')

        log.info(
            'Step 6: Redis can maintain a unique ID or count very efficiently')
        r.set('user_count', 21)
        r.incr('user_count')
        r.incr('user_count')
        r.decr('user_count')
        result = r.get('user_count')
        log.info('I could use this to generate unique ids')
        log.info(f'Redis says 21+1+1-1={result}')

        log.info('Step 7: richer data for a SKU')
        r.rpush('186675', 'chair')
        r.rpush('186675', 'red')
        r.rpush('186675', 'leather')
        r.rpush('186675', '5.99')

        log.info('Step 8: pull some data from the structure')
        cover_type = r.lindex('186675', 2)
        log.info(f'Type of cover = {cover_type}')
        '''

    except Exception as e:
        print(f'Redis error: {e}')
