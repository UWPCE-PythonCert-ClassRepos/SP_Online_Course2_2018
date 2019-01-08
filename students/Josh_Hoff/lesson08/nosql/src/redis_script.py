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
        
        log.info('ADDING CUSTOMER DATA')
        r.rpush('jackie', '360.353.3353')
        r.rpush('jackie', '98225')
        r.rpush('samantha', '253.406.2598')
        r.rpush('samantha', '91020')
        r.rpush('jordan', '360.222.5555')
        r.rpush('jordan', '89230')
        r.rpush('mike', '509.768.8099')
        r.rpush('mike', '98005')
        r.rpush('brandon', '509.253.5046')
        r.rpush('brandon', '99205')
        r.rpush('jessica', '253.789.1234')
        r.rpush('jessica', '99205')
        
        log.info('LOGGING CUSTOMER DATA')
        telephone = r.lindex('jordan', 0)
        zip_code = r.lindex('jordan', 1)
        log.info(f'Telephone: {telephone}, Zip Code: {zip_code}')

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

    except Exception as e:
        print(f'Redis error: {e}')
