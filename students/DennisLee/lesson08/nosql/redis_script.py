"""
demonstrate use of Redis
"""

import login_database
import utilities

customers = {
    'Richard Rickard': ('323-456-7890', '30498'),
    'Paul Pool': ('235-790-2468', '82910'),
    'Pamela Pomelo': ('898-676-1234', '48362'),
    'Ellen Allen': ('369-147-8642', '13658'),
    'Jill Jolly': ('503-836-5829', '97204'),
    'Bill Ball': ('774-292-3856', '03685')
}

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

        log.info('Step 5: delete from cache')
        r.delete('andy')
        email = r.get('andy')
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

        log.info('Step 9: load customer data')
        for customer, data in customers.items():
            r.rpush(customer, data[0])
            r.rpush(customer, data[1])

        log.info('Step 10: get zip code for Ellen Allen')
        zip_code = r.lindex('Ellen Allen', 1)
        log.info(f"Ellen Allen's zip code: {zip_code}")

        log.info('Step 11: get phone number for Ellen Allen')
        phone_number = r.lindex('Ellen Allen', 0)
        log.info(f"Ellen Allen's phone number: {phone_number}")

    except Exception as e:
        print(f'Redis error: {e}')
