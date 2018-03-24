"""
    demonstrate use of Redis
"""


import src.login_database
import src.utilities

def run_example():
    """
        uses non-presistent Redis only (as a cache)

    """
    log = src.utilities.configure_logger('default', 'logs/redis_script.log')


    try:
        log.info('Step 1: connect to Redis')
        r = src.login_database.login_redis_cloud()
        log.info('Step 2: cache some data in Redis')
        r.set('andy', 'andy@somewhere.com')

        log.info('Step 3: now I can read it')
        email = r.get('andy')
        log.info('But I must know the key')
        log.info(f'The results of r.get: {email}')

        log.info('Step 4: cache some more data in Redis')
        r.set('pam', 'pam@anywhere.com')
        r.set('fred', 'fred@fearless.com')

        log.info('Step 5: delete from cache')
        r.delete('andy')
        log.info(f'r.delete means andy is now: {email}')

        log.info(
            'Step 6: Redis can maintain a unique ID or count very efficiently')
        r.set('user_count', 21)
        r.incr('user_count')
        r.incr('user_count')
        r.decr('user_count')
        result = r.get('user_count')
        log.info(f'Redis says 21+1+1-1={result}')

        log.info('Step 7: richer data for a SKU')
        r.rpush('186675', 'chair')
        r.rpush('186675', 'red')
        r.rpush('186675', 'leather')
        r.rpush('186675', '5.99')

        log.info('# of SKU properties')
        r.llen('186675')

        log.info('Type of cover')
        r.lindex('186675', 2)

    except Exception as e:
        print(f'Redis error: {e}')
