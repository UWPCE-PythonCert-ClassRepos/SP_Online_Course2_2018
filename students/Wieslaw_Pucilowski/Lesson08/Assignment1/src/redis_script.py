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
        #####################################################################
        # Assignment
        #####################################################################
        log.info('Step 9: Assignment, adding new customers with phone and zip')
        r.hmset('Brandon', {'Telephone': '360-691-9021', 'Zip': '95680'})
        r.hmset('Alicia', {'Telephone': '111-255-4455', 'Zip': '98275'})
        r.hmset('Anh Tai', {'Telephone': '222-333-7768', 'Zip': '95670'})
        r.hmset('Gregory', {'Telephone': '444-967-5816', 'Zip': '98252'})
        r.hmset('Mike', {'Telephone': '555-315-3767', 'Zip': '98223'})
        r.hmset('Andrew', {'Telephone': '999-222-7777', 'Zip': '98012'})
        
        log.info('Step 10: Iterate over known hask keys')
        for i in ['Brandon', 'Alicia', 'Anh Tai', 'Gregory', 'Mike', 'Andrew']:
            print("-"*70)
            for j in r.hkeys(i):
                print("{:<20}{:<15}{:<15}".format(i, j, r.hget(i, j)))

        log.info('Step 11: Iterate over etire database')
        a, index = r.scan()

        # print(index)
        # for i in index:
            # print(i, r.type(i))

        for i in index:
            print("-"*70)
            if r.type(i) == 'hash':
                for j in r.hkeys(i):
                    print("{:<20}{:<15}{:<15}".format(i, j, r.hget(i, j)))
            elif r.type(i) == 'list':
                for j in range(r.llen(i)):
                    print("List {}, indx: {}, element: {}".format(i,j,r.lindex(i, j)))
            else:
                print("{:<20}{:<15}".format(i, r.get(i)))

        log.info('Step 12: Clear database')
        r.flushdb()

    except Exception as e:
        print(f'Redis error: {e}')
