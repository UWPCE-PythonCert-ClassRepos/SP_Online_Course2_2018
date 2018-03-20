"""
    demonstrate use of Redis
"""

import redis


def run_example():
    """
        uses non-presistent Redis only (as a cache)

    """
    try:
        credentials = login_database.get_credentials('redis_cloud')
    except Exception as e:
        print(f'Credentials error: {e}')

    try:
        logger.info('Step 1: connect to Redis')

        with login_databases.login_redis_cloud(credentials) as r:
            logger.info('Step 2: cache some data in Redis')
            r.set('andy', 'andy@somewhere.com')

            logger.info('Step 3: now I can read it')
            email = r.get('andy')
            logger.info('But I must know the key')
            logger.info(f'The results of r.get: {email}')

            logger.info('Step 4: cache some more data in Redis')
            r.set('pam', 'pam@anywhere.com')
            r.set('fred', 'fred@fearless.com')

            logger.info('Step 5: delete from cache')
            r.delete('andy')
            logger.info(f'r.delete means andy is now: {email}')

            logger.info('Step 6: Redis can maintain a unique ID or count very efficiently')
            r.set('user_count',21)
            r.incr('user_count')
            r.incr('user_count')
            r.decr('user_count')
            result = r.get('user_count')
            logger.info(f'Redis says 21+1+1-1={result}')

            logger.info('Step 7: richer data for a SKU')
            r.rpush('186675', 'chair')
            r.rpush('186675', 'red')
            r.push('186675', 'leather')
            r.rpush('186675', '5.99')

            logger.info('# of SKU properties')
            r.llen('186675')

            logger.info('Type of cover')
            r.lindex('186675', 2)

    except Exception as e:
        print(f'Redis error: {e}')
