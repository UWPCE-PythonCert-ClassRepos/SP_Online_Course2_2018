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
        log.info("Connecting to Redis")
        r = login_database.login_redis_cloud()
        log.info("Adding data.")
        r.hmset('Tom', {'name': 'Thomas Horn', 'phone': '111-111-11111', 'zip': '11111'})
        r.hmset('Ted', {'name': 'Ted H', 'phone': '222-222-2222', 'zip': '22222'})
        r.hmset('Wayne', {'name': 'Wayne P', 'phone': '333-333-3333', 'zip': '33333'})
        r.hmset('Patrick', {'name': 'Patrick B', 'phone': '444-444-4444', 'zip': '44444'})
        r.hmset('Eric', {'name': 'Eric J', 'phone': '555-555-5555', 'zip': '55555'})
        r.hmset('Bailey', {'name': 'Bailey K', 'phone': '666-666-6666', 'zip': '66666'})

        print(r.hmget('Tom', 'zip'))
        print(r.hmget('Tom', 'name'))
        print(r.hmget('Wayne', 'phone'))
        print(r.hmget('Bailey', 'zip'))


    except Exception as e:
        print(f'Redis error: {e}')


    # try:
    #     log.info('Step 1: connect to Redis')
    #     r = login_database.login_redis_cloud()
    #     log.info('Step 2: cache some data in Redis')
    #     r.set('andy', 'andy@somewhere.com')

    #     log.info('Step 2: now I can read it')
    #     email = r.get('andy')
    #     log.info('But I must know the key')
    #     log.info(f'The results of r.get: {email}')

    #     log.info('Step 3: cache more data in Redis')
    #     r.set('pam', 'pam@anywhere.com')
    #     r.set('fred', 'fred@fearless.com')

    #     log.info('Step 4: delete from cache')
    #     r.delete('andy')
    #     log.info(f'r.delete means andy is now: {email}')

    #     log.info(
    #         'Step 6: Redis can maintain a unique ID or count very efficiently')
    #     r.set('user_count', 21)
    #     r.incr('user_count')
    #     r.incr('user_count')
    #     r.decr('user_count')
    #     result = r.get('user_count')
    #     log.info('I could use this to generate unique ids')
    #     log.info(f'Redis says 21+1+1-1={result}')

    #     log.info('Step 7: richer data for a SKU')
    #     r.rpush('186675', 'chair')
    #     r.rpush('186675', 'red')
    #     r.rpush('186675', 'leather')
    #     r.rpush('186675', '5.99')

    #     log.info('Step 8: pull some data from the structure')
    #     cover_type = r.lindex('186675', 2)
    #     log.info(f'Type of cover = {cover_type}')


