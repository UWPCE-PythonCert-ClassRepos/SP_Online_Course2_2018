"""
    demonstrate use of Redis. Lesson 8 Assignment 1.
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

        log.info('Additional step 1 (Hiro): Add customer name, telephone and zip for 6 or so customers')
        # customer 1
        r.rpush('Hiro', '333-333-3333')
        r.rpush('Hiro', '55555')
        # customer 2
        r.rpush('Luis', '555-555-5555')
        r.rpush('Luis', '66666')
        # customer 3
        r.rpush('Chris', '666-666-6666')
        r.rpush('Chris', '99999')
        # customer 4
        r.rpush('Maria', '111-111-1111')
        r.rpush('Maria', '11111')
        # customer 5
        r.rpush('Tom', '222-222-2222')
        r.rpush('Tom', '22222')
        # customer 6
        r.rpush('John', '444-444-4444')
        r.rpush('John', '44444')

        log.info('Additional step 2 (Hiro): Show how you can retrieve a zip code, and then a phone number, for a known customer.')
        hiro_telephone = r.lindex('Hiro', 0)
        hiro_zipcode = r.lindex('Hiro', 1)
        log.info(f'Hiro telephone = {hiro_telephone}. Hiro Zip Code = {hiro_zipcode}')


    except Exception as e:
        print(f'Redis error: {e}')
