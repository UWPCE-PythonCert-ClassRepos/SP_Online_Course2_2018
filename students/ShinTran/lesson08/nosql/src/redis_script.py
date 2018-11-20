"""
Shin Tran
Python 220
Lesson 8 Assignment
Demonstrate use of Redis
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
        
        '''
        log.info('Step 2a: cache some data in Redis')
        r.set('andy', 'andy@somewhere.com')

        log.info('Step 2b: now I can read it')
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
        '''

        log.info('Step 2: Adding 8 customers to the data cache')
        r.hmset('Brandon', {'phone': '295-647-7874', 'zip': 57672})
        r.hmset('Bobby', {'phone': '905-306-9770', 'zip': 74089})
        r.hmset('Bryon', {'phone': '644-113-0350', 'zip': 44870})
        r.hmset('Earl', {'phone': '235-587-5642', 'zip': 40087})
        r.hmset('Kam', {'phone': '835-154-1399', 'zip': 69806})
        r.hmset('KJ', {'phone': '744-276-3597', 'zip': 75040})
        r.hmset('Jeremy', {'phone': '930-707-5099', 'zip': 49050})
        r.hmset('Richard', {'phone': '332-768-9323', 'zip': 18968})

        log.info('Step 3: Retrieve a zip code for a known customer')
        ret_zip = r.hmget('Bobby', 'zip')
        log.info(f"The zip code that Bobby resides in is {ret_zip[0]}.")

        log.info('Step 4: Retrieve a phone number for a known customer')
        ret_phone = r.hmget('KJ', 'phone')
        log.info(f"The phone number for KJ is {ret_phone[0]}.")

    except Exception as e:
        print(f'Redis error: {e}')

if __name__ == '__main__':
    run_example()
