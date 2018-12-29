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
        log.info('Step 2: cache some data in Redis')
        r.set('andy', 'andy@somewhere.com')

        log.info('Step 2: now I can read it')
        email = r.get('andy')
        log.info('But I must know the key')
        log.info(f'The results of r.get: {email}')

        log.info('Step 3: cache more data in Redis')
        r.set('pam', 'pam@anywhere.com')
        r.set('fred', 'fred@fearless.com')

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

        log.info('storing data for six users\n\n')
        r.rpush('Mike', '123-456-7890')
        r.rpush('Mike', '65464')

        r.rpush('Joe', '456-789-0123')
        r.rpush('Joe', '84744')

        r.rpush('Tyler', '890-123-4567')
        r.rpush('Tyler', '23452')

        r.rpush('Sarah', '456-767-8796')
        r.rpush('Sarah', '23545')

        r.rpush('Katie', '123-456-0034')
        r.rpush('Katie', '65222')

        r.rpush('Alex', '123-645-7890')
        r.rpush('Alex', '98111')

        user = "Alex"
        log.info(f'Retreiving data for {user}')
        user_phone = r.lindex(user, 0)
        user_zip = r.lindex(user, 1)
        log.info(f'{user} has the phone number {user_phone} and zip code '
                 f'{user_zip}')


    except Exception as e:
        print(f'Redis error: {e}')
