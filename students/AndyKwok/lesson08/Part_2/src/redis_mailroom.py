import login_database
import utilities
# import redis

def run_example():
    """
        uses non-presistent Redis only (as a cache)
    """

    log = utilities.configure_logger('default', '../logs/redis_script.log')
    
    try:
        log.info('Step 1: connect to Redis')
        r = login_database.login_redis_cloud()
        log.info('Step 2: cache some data in Redis')
        r.flushdb()
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
    log = utilities.configure_logger('default', '../logs/redis_script.log')

    try:
        r = login_database.login_redis_cloud()
        r.flushall()
        log.info('Data is being saved into redis')
        r.hmset('tester_1', {'donation': [11.0, 3.1, 23.0]})
        r.hmset('tester_3', {'donation': [10.1, 3.5, 2.0]})
        r.hmset('tester_2', {'donation': [10.0, 3, 2.0]})
        
        # log.info('Data is being read from redis')
        # result = r.hgetall('tester_1')
        # email = result['email']
        # donation = result['donation']
        # log.info('Here is are the information of one person')
        # log.info(f'Donor = {zip}')
        # log.info(f'Doantion = {donation}')

    except Exception as e:
        print(f'Redis error: {e}')

# def setdb():
    # log = utilities.configure_logger('default', '../logs/redis_script.log')
    
    # try:
        # d = login_database.login_redis_cloud()
        # d.flushall()
        # log.info('Data is being saved into redis')
        # d.hmset('andy', {'email': [11.0, 3.1, 23.0]})
        # d.hmset('pam', {'email': [10.1, 3.5, 2.0]})
        # d.hmset('fred', {'email': [10.0, 3, 2.0]})
    # except Exception as e:
        # print(f'Redis error: {e}')

        
# def redis_read_all():
# def redis_read():
# def redis_edit():
# def redis_del():
# def redis_add():
