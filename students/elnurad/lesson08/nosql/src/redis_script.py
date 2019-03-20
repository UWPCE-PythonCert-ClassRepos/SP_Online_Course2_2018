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

    # try:
    #     log.info('Step 1: connect to Redis')
    #     r = login_database.login_redis_cloud()
    #     log.info('Step 2: cache some data in Redis')
    #     r.set('andy', 'andy@somewhere.com')

    #     log.info('Step 2: now I can read it')
    #     email = r.get('andy')
    #     log.info('But I must know the key')
    #     log.info(f'The results of r.get: {email}')

    #     log.info('Step 3: cache more data in Redis')
    #     r.set('pam', 'pam@anywhere.com')
    #     r.set('fred', 'fred@fearless.com')

    #     log.info('Step 4: delete from cache')
    #     r.delete('andy')
    #     log.info(f'r.delete means andy is now: {email}')

    #     log.info(
    #         'Step 6: Redis can maintain a unique ID or count very efficiently')
    #     r.set('user_count', 21)
    #     r.incr('user_count')
    #     r.incr('user_count')
    #     r.decr('user_count')
    #     result = r.get('user_count')
    #     log.info('I could use this to generate unique ids')
    #     log.info(f'Redis says 21+1+1-1={result}')

    #     log.info('Step 7: richer data for a SKU')
    #     r.rpush('186675', 'chair')
    #     r.rpush('186675', 'red')
    #     r.rpush('186675', 'leather')
    #     r.rpush('186675', '5.99')

    #     log.info('Step 8: pull some data from the structure')
    #     cover_type = r.lindex('186675', 2)
    #     log.info(f'Type of cover = {cover_type}')

    # except Exception as e:
    #     print(f'Redis error: {e}')

        # Add some customer data to the cache, Have Redis store a customer name, telephone 
        # and zip for 6 or so customers. Then show how you can retrieve a zip code, and then a phone number, for a known customer.
    try:
        log.info('Step 1: connect to Redis')
        r = login_database.login_redis_cloud()
        log.info('Step 2: cache some data in Redis')
        r.hmset('Heidi', {'tel': '235-343-8934', 'zip': '89707'})
        r.hmset('Leon', {'tel': '566-895-8522', 'zip': '41525'})
        r.hmset('Peter', {'tel': '345-434-5444','zip': '43433'})
        r.hmset('Diane', {'tel': '456-343-3898', 'zip': '21009'})
        r.hmset('Katja', {'tel': '234-439-8432', 'zip': '21003'})
        r.hmset('Mary', {'tel': '344-233-2856', 'zip': '78677'})


        log.info('Step 2: now I can read it')
        tel = r.hmget('Heidi', 'tel')
        log.info('But I must know the key')
        log.info(f'The results of r.hmget: {tel}')
        heidi_zip = r.hmget('Heidi', 'zip')
        log.info(f"Heidi's results of r.hmget: {heidi_zip}")

        leon_tel = r.hmget('Leon', 'tel')
        leon_zip = r.hmget('Leon', 'zip')
        log.info(f"Leon's results are: tel: {leon_tel}, zip: {leon_zip}")

        peter_tel = r.hmget('Peter', 'tel')
        peter_zip = r.hmget('Peter', 'zip')
        log.info(f"Peter's results are: tel: {peter_tel}, zip: {peter_zip}")

        diane_tel = r.hmget('Diane', 'tel')
        diane_zip = r.hmget('Diane', 'zip')
        log.info(f"Diane's results are: tel: {diane_tel}, zip: {diane_zip}")

        katja_tel = r.hmget('Katja', 'tel')
        katja_zip = r.hmget('Katja', 'zip')
        log.info(f"Katja's results are: tel: {katja_tel}, zip: {katja_zip}")

        mary_tel = r.hmget('Mary', 'tel')
        mary_zip = r.hmget('Mary', 'zip')
        log.info(f"Mary's results are: tel: {mary_tel}, zip: {mary_zip}")

    except Exception as e:
        print(f'Redis error: {e}')