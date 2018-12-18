"""
    demonstrate use of Redis
"""


import login_database
import utilities
import json


def run_example():
    """
        uses non-presistent Redis only (as a cache)

    """

    log = utilities.configure_logger('default', '../logs/redis_script.log')

    try:
        log.info('Step 1: connect to Redis')
        r = login_database.login_redis_cloud()
        log.info('Step 2: cache some data in Redis')
        r.set('andy', json.dumps({'email': 'andy@somewhere.com', 'phone': '123-123-1234', 'zip': '1234zip'}))

        # r.set('andy', 'andy@somewhere.com')

        log.info('Step 2: now I can read it')
        result = r.get('andy')
        # result = json.loads(result)
        log.info('But I must know the key')
        log.info(f'The results of r.get: {result}')

        log.info('Step 3: cache more data in Redis')
        r.set('pam', json.dumps({'email': 'pam@anywhere.com', 'phone': '111-123-1234', 'zip': '1234zip'}))
        r.set('fred', json.dumps({'email': 'fred@fearless.com', 'phone': '000-123-1234', 'zip': '00001'}))
        r.set('will', json.dumps({'email': 'williamwhite@gmail.com', 'phone': '222-123-1234', 'zip': '00002'}))
        r.set('monet', json.dumps({'email': 'monet@gmail.com', 'phone': '333-123-1234', 'zip': '00003'}))
        r.set('roscoe', json.dumps({'email': 'roscoe@gmail.com', 'phone': '444-123-1234', 'zip': '00004'}))
        r.set('reggie', json.dumps({'email': 'reggie@gmail.com', 'phone': '555-123-1234', 'zip': '00005'}))
        r.set('sherman', json.dumps({'email': 'sherman@gmail.com', 'phone': '666-123-1234', 'zip': '00006'}))
        r.set('brhey', json.dumps({'email': 'brhey@gmail.com', 'phone': '777-123-1234', 'zip': '00007'}))

        log.info('grab Shermans zip code and phone number')
        result = r.get('sherman')
        result = json.loads(result)
        log.info(f'Shermans zip: {result["zip"]}')
        log.info(f'Shermans phone number: {result["phone"]}')


        log.info('Step 4: delete from cache')
        r.delete('andy')
        log.info(f'r.delete means andy is now: {result}')

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
