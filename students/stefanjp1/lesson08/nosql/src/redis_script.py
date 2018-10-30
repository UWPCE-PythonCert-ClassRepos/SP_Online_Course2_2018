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
        
        log.info('** Add more customer data to cache')
        r.hmset('Stefan', {'Telephone': '555-943-4167', 'Zip': '98118'})
        r.hmset('Mason', {'Telephone': '555-865-3262', 'Zip': '98118'})
        r.hmset('Donald', {'Telephone': '555-901-8586', 'Zip': '11002'})
        r.hmset('Coolio', {'Telephone': '555-867-5309', 'Zip': '20221'})
        r.hmset('Pam', {'Telephone': '555-901-9988', 'Zip': '98765'})
        
        log.info('** Get customer zip, then telephone and log it')
        Stefan_zip = r.hmget('Stefan', 'Zip')
        Stefan_telephone = r.hmget('Stefan', 'Telephone')
        log.info(f'Stefan Zip is {Stefan_zip} and Telephone number is {Stefan_telephone}')

    except Exception as e:
        print(f'Redis error: {e}')
