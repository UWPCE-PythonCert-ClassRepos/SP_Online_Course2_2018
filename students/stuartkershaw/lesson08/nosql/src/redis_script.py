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
        r.set('andy_name', 'Andy')
        r.set('andy_phone', '1-206-555-0000')
        r.set('andy_zip', '98100')
        r.set('james_name', 'James')
        r.set('james_phone', '1-206-555-0001')
        r.set('james_zip', '98101')
        r.set('stuart_name', 'Stuart')
        r.set('stuart_phone', '1-206-555-0002')
        r.set('stuart_zip', '98102')
        r.set('cayce_name', 'Cayce')
        r.set('cayce_phone', '1-206-555-0003')
        r.set('cayce_zip', '98103')
        r.set('sarah_name', 'Sarah')
        r.set('sarah_phone', '1-206-555-0004')
        r.set('sarah_zip', '98104')
        r.set('christina_name', 'Christina')
        r.set('christina_phone', '1-206-555-0005')
        r.set('christina_zip', '98105')

        log.info('Step 2: now I can read it')
        andy_phone = r.get('andy_phone')
        andy_zip = r.get('andy_zip')
        log.info('But I must know the key')
        log.info(f'The results of r.get andy_phone: {andy_phone}')
        log.info(f'The results of r.get andy_zip: {andy_zip}')

        log.info('Step 3: cache more data in Redis')
        r.set('pam_name', 'Pam')
        r.set('pam_phone', '1-206-555-0006')
        r.set('pam_zip', '98106')
        r.set('fred_name', 'Fred')
        r.set('fred_phone', '1-206-555-0007')
        r.set('fred_zip', '98107')

        log.info('Step 4: delete from cache')
        r.delete('andy_phone')
        r.delete('andy_zip')
        andy_phone = r.get('andy_phone')
        andy_zip = r.get('andy_zip')
        log.info(f'r.delete means andy_phone is now: {andy_phone}')
        log.info(f'r.delete means andy_zip is now: {andy_zip}')

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

    except Exception as e:
        print(f'Redis error: {e}')
