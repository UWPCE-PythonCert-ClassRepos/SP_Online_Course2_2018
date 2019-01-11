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

def run_nosql_ex():
    """
        redis data lesson 08
    """

    log = utilities.configure_logger('default', '../logs/redis_script.log')

    try:
        r = login_database.login_redis_cloud()
        r.flushall()
        log.info('Data is being saved into redis')
        r.hmset('andy', {'email': 'andy@somewhere.com', 'zip': '91700', 'phone': '555-666-8888'})
        r.hmset('pam', {'email': 'pam@anywhere.com', 'zip': '91755', 'phone': '322-666-8888'})
        r.hmset('fred', {'email': 'fred@fearless.com', 'zip': '98534', 'phone': '555-666-2888'})
        r.hmset('tester_1', {'email': 'test1@fearless.com', 'zip': '91755', 'phone': '555-666-8788'})
        r.hmset('tester_3', {'email': 'test3@fearless.com', 'zip': '91755', 'phone': '555-666-8787'})
        r.hmset('tester_2', {'email': 'test2@fearless.com', 'zip': '91785', 'phone': '555-666-8799'})
        
        log.info('Data is being read from redis')
        result = r.hgetall('tester_1')
        email = result['email']
        zip = result['zip']
        phone = result['phone']
        log.info('Here is are the information of one person')
        log.info(f'tester_1 - email = {email}')
        log.info(f'tester_1 - zip = {zip}')
        log.info(f'tester_1 - phone= {phone}')

    except Exception as e:
        print(f'Redis error: {e}')