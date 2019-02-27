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

        log.info('Add customers to cache')
        r.rpush('customer_one', '111-111-1111', '1111' )
        r.rpush('customer_two', '111-111-1112', '22222' )
        r.rpush('customer_three', '111-111-1113', '33333' )
        r.rpush('customer_four', '111-111-1114', '44444' )
        r.rpush('customer_five', '111-111-1115', '55555' )
        r.rpush('customer_six', '111-111-1116', '66666' )

        log.info('Retrieve Zip Code customer_three')
        zip = r.lindex('customer_three', 1)
        print("\nzip code: ", zip)
        log.info('Retrieve Phone customer_three')
        phone = r.lindex('customer_three',0)
        print('\nphone:', phone)
        x=r.llen('customer_three')
        log.info('Retrieve customer_three elements')
        print('\nall elements customer_three:')
        for i in range(0, x):
            print(r.lindex('customer_three',i))

        r.flushdb()

    except Exception as e:
        print(f'Redis error: {e}')
