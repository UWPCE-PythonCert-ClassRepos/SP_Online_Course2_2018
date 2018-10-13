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

        log.info('Step 9: Add customer for 6 customers: name, telephone, and ZIP')
        r.rpush('Cary Grant', '555-123-4567')
        r.rpush('Cary Grant', '12345')

        r.rpush('James Stewart', '555-234-5678')
        r.rpush('James Stewart', '23456')

        r.rpush('Audrey Hepburn', '555-345-6789')
        r.rpush('Audrey Hepburn', '34567')

        r.rpush('Katherine Hepburn', '555-456-7890')
        r.rpush('Katherine Hepburn', '45678')

        r.rpush('Grace Kelly', '555-567-8901')
        r.rpush('Grace Kelly', '56789')

        r.rpush('Kim Novak', '555-678-9012')
        r.rpush('Kim Novak', '67890')

        log.info("Step 10: Get a known cusomter's ZIP and phone")
        jimmy_phone = r.lindex('James Stewart', 0)
        jimmy_ZIP = r.lindex('James Stewart', 1)
        log.info(f"Phone number is {jimmy_phone}, ZIP code is {jimmy_ZIP}")

    except Exception as e:
        print(f'Redis error: {e}')
