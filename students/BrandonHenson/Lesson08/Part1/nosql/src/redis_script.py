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

        log.info('Step 3: now I can read it')
        email = r.get('andy')
        log.info('But I must know the key')
        log.info(f'The results of r.get: {email}')

        log.info('Step 4: cache more data in Redis')
        r.set('pam', 'pam@anywhere.com')
        r.set('fred', 'fred@fearless.com')

        log.info('Step : delete from cache')
        r.delete('andy')
        log.info(f'r.delete means andy is now: {email}')

        log.info('Step 6: Redis can maintain a unique ID or count very efficiently')
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
        
        log.info('Add')
        r.hmset('Brandon', {'Telephone': '360-691-9021', 'Zip': '95680'})
        r.hmset('Alicia', {'Telephone': '425-355-3355', 'Zip': '98275'})
        r.hmset('Michael', {'Telephone': '360-722-9768', 'Zip': '95670'})
        r.hmset('Brandon Jr', {'Telephone': '360-967-5816', 'Zip': '98252'})
        r.hmset('Kaiya', {'Telephone': '425-315-3797', 'Zip': '98223'})
        Alicia_phone = r.hmget('Alicia', 'Telephone')
        Kaiya_zip = r.hmget('Kaiya', 'Zip')
        Michael_phone = r.hmget('Michael', 'Telephone')
        log.info(f'Alicia\'s Telephone number is : {Alicia_phone}')
        log.info(f'Kaiya\'s Zip is: {Kaiya_zip}')
        

    except Exception as e:
        print(f'Redis error: {e}')

