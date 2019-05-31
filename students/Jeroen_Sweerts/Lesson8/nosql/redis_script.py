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

    except Exception as e:
        print(f'Redis error: {e}')
        
        

def redis_assignment_create():
    log = utilities.configure_logger('default', 'logs/redis_script.log')

    try:
        log.info('Step 1: connect to Redis')
        r = login_database.login_redis_cloud()
        phoneidx = 0
        zipidx = 1

        r.rpush('Jeroen', 15555222)
        r.rpush('Jeroen', 2800)

        r.rpush('Heinz', 2001589)
        r.rpush('Heinz', 1000)

        r.rpush('Knudde', 3658714)
        r.rpush('Knudde', 6900)

        r.rpush('Gaston', 22222221111)
        r.rpush('Gaston', 98139)

        r.rpush('Neintje', 121212129)
        r.rpush('Neintje', 7000)

        r.rpush('Bumbalu', 31346546)
        r.rpush('Bumbalu', 9999)
        phone = r.lindex('Jeroen', phoneidx)
        log.info(f'Jeroen Phone Number = {phone}')
        zipcode = r.lindex('Jeroen', zipidx)
        log.info(f'Jeroen Zip Code = {zipcode}')
    except Exception as e:
        print(f'Redis error: {e}')




