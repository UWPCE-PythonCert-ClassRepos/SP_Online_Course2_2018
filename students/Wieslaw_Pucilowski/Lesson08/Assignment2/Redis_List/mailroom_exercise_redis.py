import redis
import utilities
import login_database
# import donor_data
import pprint
import json

pp = pprint.PrettyPrinter(width=120)
from pymongo.errors import OperationFailure

__author__ = "Wieslaw Pucilowski"

pp = pprint.PrettyPrinter(width=120)

log = utilities.configure_logger('default', '../logs/redis_script.log')

class Main():
    def populate_db():
        log.info('*** Inside populate_db()')
        # try:
        log.info('Step 1: connect to Redis')
        r = login_database.login_redis_cloud()
        
        log.info('Step 2: cache some data in Redis')
        # donor's hash
        name = 'Brandon Henson'
        r.hmset(name,
                {   'Telephone': '425-355-3355',
                    'Zip': '98275',
                    # 'Donations' : [100, 200], # <-- does not work here !
                    'email': 'bigbrandonh@ggmail.com'
                }
            )
        # donor donations list per donor
        donors_donations = '_'.join(name.split())
        r.rpush(donors_donations, 100)
        r.rpush(donors_donations, 200)

        # log.info('Step 12: Clear database')
        # r.flushdb()
        
        # except Exception as e:
        #     print(f'Redis error: {e}')
    def report():
        log.info('*** Inside report()')
        log.info('Step 1: connect to Redis')
        r = login_database.login_redis_cloud()
        
        name = 'Brandon Henson'
        donors_donations = '_'.join(name.split())
        for i in [name]:
            for j in r.hkeys('Brandon Henson'):
                print("{:<20}{:<15}{:<15}".format(i, j, r.hget(i, j)))
        
        print("{} donations:".format(name))
        for i in [donors_donations]:
            for j in range(r.llen(i)):
                print("{} donation # {} : {}".format(i,j+1,r.lindex(i, j)))
            print("Number of donation: {}".format(r.llen(i)))
            print("Total of {} donations: {}".format(i, sum([int(x) for x in r.lrange(i, 0, r.llen(i))]
                                                                )
                                                     )
                  )
            print("Average of {} donations: {}".format(i, sum([int(x) for x in r.lrange(i, 0, r.llen(i))]
                                                                ) / r.llen(i)
                                                     )
                  )
            
    def clear_db():
        log.info('*** Inside celar_db()')
        log.info('Step 1: connect to Redis')
        r = login_database.login_redis_cloud()
        log.info('Step 12: Clear database')
        r.flushdb()

if __name__ == '__main__':
    Main.populate_db()
    Main.report()
    Main.clear_db()