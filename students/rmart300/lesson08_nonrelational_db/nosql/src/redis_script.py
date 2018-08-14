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

        log.info('Step 7: richer data for a SKU')
        r.rpush(1, 'Mark')
        r.rpush(1, '27890')
        r.rpush(1, '336-980-9878')
        r.rpush(2, 'Tom')
        r.rpush(2, '94920')
        r.rpush(2, '414-215-6674')
        r.rpush(3, 'Steve')
        r.rpush(3, '27360')
        r.rpush(3, '336-688-0961')
        r.rpush(4, 'Che')
        r.rpush(4, '32456')
        r.rpush(4, '331-481-4509')
        r.rpush(5, 'Ashley')
        r.rpush(5, '91910')
        r.rpush(5, '987-234-0978')
        r.rpush(6, 'Kelly')
        r.rpush(6, '45671')
        r.rpush(6, '607-802-8222')


        log.info('Step 8: pull some data from the structure')
        for i in range(1,7):
            cust_name = r.lindex(i,0)
            cust_zip = r.lindex(i,1)
            cust_phone = r.lindex(i, 2)
            log.info(f'{cust_name} zip = {cust_zip}; phone num = {cust_phone}')

    except Exception as e:
        print(f'Redis error: {e}')
