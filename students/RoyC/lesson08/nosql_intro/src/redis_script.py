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

        log.info('Step 9: add users with phone # and zip code')
        r.hmset('Bugs Bunny', {'Phone':'800-214-1234', 'Zip_Code':'98042'})
        r.hmset('Porky Pig', {'Phone':'999-555-1212', 'Zip_Code':'98031'})
        r.hmset('Foghorn Leghorn', {'Phone':'805-637-7032', 'Zip_Code':'93454'})
        r.hmset('Tweety Bird', {'Phone':'425-222-333', 'Zip_Code':'90210'})
        r.hmset('Elmer Fudd', {'Phone':'900-315-7654', 'Zip_Code':'99888'})

        log.info('Step 10: Get phone and zip for user')
        data = r.hgetall('Foghorn Leghorn')
        log.info(f'Foghorn Leghorn info: Phone #: {data["Phone"]} Zip Code: {data["Zip_Code"]}')

    except Exception as e:
        print(f'Redis error: {e}')
