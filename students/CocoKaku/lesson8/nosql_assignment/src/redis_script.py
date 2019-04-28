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

    except Exception as e:
        print(f'Redis error: {e}')

def run_exercise():
    """
    redis exercise

    Assignment:
    Add some customer data to the cache.
    Have Redis store a customer name, telephone and zip for 6 or so customers.
    Then show how you can retrieve a zip code, and then a phone number, for a known customer.
    """

    log = utilities.configure_logger('default', '../logs/redis_script.log')

    try:
        log.info('Step 1: connect to Redis')
        r = login_database.login_redis_cloud()

        log.info('Step 2: cache customer data in Redis')
        r.rpush('Mark', '808-555-1234', '96825')
        r.rpush('Roger', '717-123-4567', '17331')
        r.rpush('Tom', '425-222-1234', '98275')
        r.rpush('Mimi', '206-999-9999', '98101')
        r.rpush('Maureen', '212-867-5309', '10002')
        r.rpush('Joanne', '617-542-3779', '02114')

        log.info('Step 3: read customer info')
        log.info(f"Roger's phone number is {r.lindex('Roger',2)}, and his zipcode is {r.lindex('Roger', 1)}.")
        log.info(f"Mark's phone number is {r.lindex('Mark',2)}, and his zipcode is {r.lindex('Mark', 1)}.")

    except Exception as e:
        print(f'Redis error: {e}')
