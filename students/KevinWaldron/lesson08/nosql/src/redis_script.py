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

        log.info('Step 9: add some extra users with more data')
        r.hmset('Bill S. Preston', {'Number':'253-363-3847', 'Zip-Code':'98053'})
        r.hmset('Ted Theodore Logan', {'Number':'253-363-3848', 'Zip-Code':'98054'})
        r.hmset('Abe Lincoln', {'Number':'253-363-3849', 'Zip-Code':'98055'})
        r.hmset('Sissy Sis', {'Number':'253-363-3850', 'Zip-Code':'98056'})
        r.hmset('Lilly Li', {'Number':'253-363-3851', 'Zip-Code':'98057'})
        r.hmset('Cindy Ci', {'Number':'253-363-3852', 'Zip-Code':'98058'})

        log.info('Step 10: Get phone and zip for user')
        data = r.hgetall('Lilly Li')
        log.info(f'Lilly Li Phone: {data["Number"]} Zip: {data["Zip-Code"]}')

    except Exception as e:
        print(f'Redis error: {e}')
