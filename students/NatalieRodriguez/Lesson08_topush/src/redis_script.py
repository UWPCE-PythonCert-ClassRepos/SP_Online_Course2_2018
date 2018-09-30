"""
    demonstrate use of Redis
"""


import login_db
import utilities


def run_example():
    """
        Redis

    """

    log = utilities.configure_logger('default', '../logs/redis_script.log')

    try:
        log.info('Step 1: connect to Redis')
        r = login_db.login_redis_cloud()
        log.info('Step 2: cache data in db')
        r.set('natalie', 'natalie@gmail.com')

        log.info('Step 2: Add some data to the cache')
        r.hmset('Luke', {'phone': '319-706-8805', 'age': 29})
        r.hmset('Virgil', {'phone': '913-366-2202', 'age': 15})
        r.hmset('River', {'phone': '972-310-1058', 'age': 36})
        r.hmset('Kibson', {'phone': '309-304-0112', 'age': 5})

        log.info('Step 3: Return Virgil\'s phone number')
        phone_virgil = r.hmget('Virgil', 'phone')
        log.info(f'Virgil\'s phone number: {phone_virgil}')

        log.info('Step 4: Get Virgil\'s')
        age_virgil = r.hmget('Virgil', 'age')
        log.info(f'Virgil\'s age: {age_Virgil}')

    except Exception as e:
        print(f'Redis error: {e}')