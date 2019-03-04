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

        log.info('Step 9: (assignment) add customer name, telephone, zip. Display zip and number for customer.')
        r.hmset('Adam', {'phone':'123-555-1234', 'zip':'74012'})
        r.hmset('Drew', {'phone':'123-555-2460', 'zip':'73160'})
        r.hmset('Brent', {'phone':'123-555-1337', 'zip':'74077'})
        r.hmset('Josh', {'phone':'123-555-9874', 'zip':'73135'})
        r.hmset('Jake', {'phone':'123-555-8888', 'zip':'81234'})
        r.hmset('Kyle', {'phone':'123-555-6542', 'zip':'74078'})

        name_dict = r.hgetall('Adam')
        phone = name_dict['phone']
        log.info(f'Adams phone is {phone}')
        zip_code = name_dict['zip']
        log.info(f'Adams zip is {zip_code}')


    except Exception as e:
        print(f'Redis error: {e}')
