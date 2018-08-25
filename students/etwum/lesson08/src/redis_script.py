"""
    demonstrate use of Redis
"""


import src.login_database as ld
import src.utilities as ut


def run_example():
    """
        uses non-presistent Redis only (as a cache)

    """

    log = ut.configure_logger('default', '../logs/redis_script.log')

    try:
        log.info('Step 1: connect to Redis')
        r = ld.login_redis_cloud()

        log.info('Step 2: cache some data in Redis')
        r.hmset('Customer 1', {'name': 'Mike','phone number': '425-432-4324', 'zip code': 98105})
        r.hmset('Customer 2', {'name': 'Joe', 'phone number': '425-324-4325', 'zip code': 98125})
        r.hmset('Customer 3', {'name': 'Tom', 'phone number': '206-567-4207', 'zip code': 98101})
        r.hmset('Customer 4', {'name': 'Manny', 'phone number': '404-764-9385', 'zip code': 30096})
        r.hmset('Customer 5', {'name': 'Seth', 'phone number': '306-462-4394', 'zip code': 85748})
        r.hmset('Customer 6', {'name': 'Ben', 'phone number': '957-124-9845', 'zip code': 90193})

        log.info('Step 3: Get customer name and zip code')
        zip_code = r.hmget('Customer 2', 'zip code')
        name_cust2 = r.hmget('Customer 2', 'name')
        log.info(f"Here is {name_cust2} phone number: {zip_code}")

        log.info('Step 3: Get customer name and phone number')
        number = r.hmget('Customer 1', 'phone number')
        name_cust1 = r.hmget('Customer 1', 'name')
        log.info(f"Here is {name_cust1} phone number: {number}")

        """log.info('Step 2: now I can read it')
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
        log.info(f'Type of cover = {cover_type}')"""

    except Exception as e:
        print(f'Redis error: {e}')
