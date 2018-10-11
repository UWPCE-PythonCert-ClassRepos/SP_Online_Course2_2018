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
    input('Redis Example. Press enter to continue...........')
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

        log.info('Step 6: Redis can maintain a unique ID or '
                 'count very efficiently')
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

        log.info('Assignment: Add some customer data to the cache.\n'
                 ' Have Redis store a customer name, telephone and zip\n'
                 ' for 6 or so customers. Then show how you can retrieve\n '
                 'a zip code, and then a phone number, for a known customer.')
        log.info('flushing the db first..........')
        r.flushdb()
        r.flushall()
        cust_data = [('drew', '555-555-1234', '60606'),
                     ('matt', '555-555-1111', '60605'),
                     ('emmy', '555-555-2222', '60216'),
                     ('liz', '555-555-3334', '34503'),
                     ('nico', '555-555-4444', '34503'),
                     ('scott', '555-555-5432', '60606'),
                     ('sharon', '555-555-9857', '34503')]
        for name, num, zip_code in cust_data:
            log.info(name + ' ' + num + ' ' + zip_code)
            r.hmset(name, {'phone_num': num, 'zip': zip_code})
            
            phone_num = r.hget(name, 'phone_num')
            zippy = r.hget(name, 'zip')
            log.info(name + ' phone number: ' + phone_num)
            log.info(name + ' zip code: ' + zippy)

    except Exception as e:
        print(f'Redis error: {e}')
