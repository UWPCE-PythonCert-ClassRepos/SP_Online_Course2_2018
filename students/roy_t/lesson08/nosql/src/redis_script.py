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


        log.info('ASSIGNMENT: store customer data')
        r.rpush('Franklin Tulipvelt', '111-555-1212')
        r.rpush('Franklin Tulipvelt', '99888')
        r.rpush('Poppy McGee', '111-555-1343')
        r.rpush('Poppy McGee', '99888')
        r.rpush('Pat Nosayjak', 'Unknown')
        r.rpush('Pat Nosayjak', 'Unknown')
        r.rpush('Chris Rockerford', '111-555-1211')
        r.rpush('Chris Rockerford', '99811')
        r.rpush('Mary Littlelamb', '111-555-1111')
        r.rpush('Mary Littlelamb', '99811')
        r.rpush('Georgia Peach', '111-555-3232')
        r.rpush('Georgia Peach', '99811')

        log.info('ASSIGNMENT: pull some customer data from the structure')
        customer_names = ['Franklin Tulipvelt', 'Poppy McGee', 'Pat Nosayjak',
                            'Chris Rockerford', 'Mary Littlelamb', 'Georgia Peach']

        for customer in customer_names:
            phone = r.lindex(customer, 0)
            zipcode = r.lindex(customer, 1)
            log.info(f'ASSIGNMENT: Customer Name: {customer} Zip: {zipcode} Phone: {phone}')

        log.info('ASSIGNMENT: Printing only Poppy McGee\'s information:')
        for customer in customer_names:
            phone = r.lindex(customer, 0)
            zipcode = r.lindex(customer, 1)
            if customer == 'Poppy McGee':
                log.info(f'ASSIGNMENT: Customer Name: {customer} Zip: {zipcode} Phone: {phone}')

    except Exception as e:
        print(f'Redis error: {e}')
