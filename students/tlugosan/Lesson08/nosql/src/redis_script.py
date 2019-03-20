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
        # log.info('Step 2: cache some data in Redis')
        # r.set('andy', 'andy@somewhere.com')
        #
        # log.info('Step 2: now I can read it')
        # email = r.get('andy')
        # log.info('But I must know the key')
        # log.info(f'The results of r.get: {email}')
        #
        # log.info('Step 3: cache more data in Redis')
        # r.set('pam', 'pam@anywhere.com')
        # r.set('fred', 'fred@fearless.com')
        #
        # log.info('Step 4: delete from cache')
        # r.delete('andy')
        # log.info(f'r.delete means andy is now: {email}')
        #
        # log.info(
        #     'Step 6: Redis can maintain a unique ID or count very efficiently')
        # r.set('user_count', 21)
        # r.incr('user_count')
        # r.incr('user_count')
        # r.decr('user_count')
        # result = r.get('user_count')
        # log.info('I could use this to generate unique ids')
        # log.info(f'Redis says 21+1+1-1={result}')
        #
        # log.info('Step 7: richer data for a SKU')
        # r.rpush('186675', 'chair')
        # r.rpush('186675', 'red')
        # r.rpush('186675', 'leather')
        # r.rpush('186675', '5.99')
        #
        # log.info('Step 8: pull some data from the structure')
        # cover_type = r.lindex('186675', 2)
        # log.info(f'Type of cover = {cover_type}')

        log.info('Add 6 more customers entry with their name, phone number '
                 'and zip code')
        r.hmset('Maria', {'phone': '555-123-1111', 'zip': '98034'})
        r.hmset('David', {'phone': '555-123-2222', 'zip': '98033'})
        r.hmset('Gary', {'phone': '555-123-3333', 'zip': '98104'})
        r.hmset('Bruno', {'phone': '555-123-4444', 'zip': '98052'})
        r.hmset('Anna', {'phone': '555-123-5555', 'zip': '93423'})
        r.hmset('Victoria', {'phone': '555-123-6666', 'zip': '94122'})

        log.info('Retrieving Maria\'s phone number')
        maria_phone = r.hmget('Maria', 'phone')
        log.info(f'Mary phone number : {maria_phone}')

        log.info('Get all info associated to Gary')
        test_gary = r.hgetall('Gary')
        log.info(f'{test_gary}')
        log.info('Get Gary\'s number')
        gary_phone = test_gary['phone']
        log.info(f'{gary_phone}')
        log.info("Get Gary\'s zip number")
        gary_zip = test_gary['zip']
        log.info(f'{gary_zip}')

        log.info('Get all the keys associated to Gary')
        the_keys = r.hkeys('Gary')
        log.info(f'{the_keys}')


    except Exception as e:
        print(f'Redis error: {e}')
