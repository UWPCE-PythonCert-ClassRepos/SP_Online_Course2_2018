'''
Sean Tasaki
11/27/2018
Lesson08
'''

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

        log.info('Add Customer Info')
        r.hmset('Beet', {'Telephone': '808-543-9021', 'Zip': '96701'})
        r.hmset('Ujido', {'Telephone': '808-355-5678', 'Zip': '11211'})
        r.hmset('Sean', {'Telephone': '524-444-4321', 'Zip': '12111'})
        r.hmset('Anna', {'Telephone': '321-555-6790', 'Zip': '23456'})
        r.hmset('Alaska', {'Telephone': '123-456-7890', 'Zip': '98223'})
        sean_phone = r.hmget('Sean', 'Telephone')
        Ujido_zip = r.hmget('Ujido', 'Zip')
        anna_zip = r.hmget('Anna', 'Zip')
        log.info(f'Sean\'s Telephone number is : {sean_phone}')
        log.info(f'Ujido\'s Zip is: {Ujido_zip}')
        log.info(f'Anna\'s Zip is: {anna_zip}')

    except Exception as e:
        print(f'Redis error: {e}')
