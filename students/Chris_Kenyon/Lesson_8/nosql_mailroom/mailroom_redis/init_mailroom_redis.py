import login_database
import utilities
import os

log = utilities.configure_logger('default', '../mongo_mailroom.log')


def init_redis():
    """
    connect to redis and setup initial data
    """
    try:
        log.info('Step 1: connect to Redis')
        r = login_database.login_redis_cloud()
        r.flushdb()
        
        r.hmset("Justin Thyme", {'Donation': '1, 1, 1', 'Email': 'Justin.Thyme@email.com'}),
        r.hmset("Beau Andarrow", {'Donation': '207.121324, 400.321234, 12345.001234', 'Email': 'Beau.Andarrow@email.com'}),
        r.hmset("Crystal Clearwater", {'Donation': '80082', 'Email': 'Crystal.Clearwater@email.com'}),
        r.hmset("Harry Shins", {'Donation': '1.00, 2.00, 3.00', 'Email': 'Harry.Shins@email.com'}),
        r.hmset("Bob Zuruncle", {'Donation': '0.53, 7.00', 'Email': 'Bob.Zuruncle@email.com'}),
        r.hmset("Al Kaseltzer", {'Donation': '1010101, 666.00', 'Email': 'Al.Kaseltzer@email.com'}),
        r.hmset("Joe Somebody", {'Donation': '25', 'Email': 'Joe.Somebody@email.com'})    
    
    except Exception as e:
        log.info(f'Error message: {e}')    

if __name__ == '__main__':
    init_redis()