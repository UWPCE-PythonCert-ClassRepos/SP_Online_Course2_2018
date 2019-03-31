"""
    demonstrate use of Redis
"""
import login_database
import learn_data
import utilities
import logging
import pprint
from collections import defaultdict
from copy import deepcopy

id="_data"
log = utilities.configure_logger('default', '../logs/redis_script.log')
try:
    log.info('Step: connect to Redis')
    r = login_database.login_redis_cloud()
except Exception as e:
    print(f'Redis error: {e}')

def setup_data_redis():
    """ converd data to be used by redis"""
    donation_database = learn_data.donation_data()
    lst_donations=[]
    for elem in donation_database:
        temp=[]
        for key, value in elem.items():
            temp.append(value)
        lst_donations.append(temp)
    return (lst_donations)

def setup_database():
    """uses non-presistent Redis only (as a cache)"""
    donations=setup_data_redis()

    try:
        log.info('Step: cache donor data in Redis')
        for elem in donations:
            d=elem[0]
            d_data=d+id
            r.rpush(d_data,elem[2],elem[3])
            for i in elem[1]:
                r.rpush(d,i)

    except Exception as e:
        print(f'Redis error: {e}')
    return

def add_donor(donor,email='generic@generic.com', phone='000-000-0000'):
    """ add donor"""
    try:
        log.info('Step: connect to Redis')
        log.info('Step: add donor to Redis')
        if not r.exists(donor):
            r.rpush(donor,0)
            donord=donor+id
            r.rpush(donord,email,phone)
    except Exception as e:
        print(f'Redis error: {e}')
    return

def add_donation(donor,amount='0'):
    """ add donor"""
    try:
        log.info('Step: connect to Redis')
        log.info('Step: add donation to Redis')
        don=[]
        if r.exists(donor):
            r.rpush(donor,amount)
            for i in range(0, r.llen(donor)):
                don.append(r.lindex(donor, i))
            if don[0]=='0':
                r.lpop(donor)
    except Exception as e:
        print(f'Redis error: {e}')
    return

def delete_donation(donor,amount):
    """ delete donation: complex logic:
        -identify if donor exists
        -create local list of all donations_data
        -check if donation exists
        -remove all the donations from redis and reload the list except deleted
    """
    try:
        log.info('Step: connect to Redis')
        log.info('Step: delete donation to Redis')
        don=[]
        amount=str(amount)
        if r.exists(donor):
            for i in range(0, r.llen(donor)):
                don.append(r.lindex(donor, i))
            if amount in don:
                don.remove(amount)
                if len(don)==0:
                    don.append('0')
                for i in range(0, r.llen(donor)):
                    r.lpop(donor)
                for i in don:
                    r.rpush(donor,i)
    except Exception as e:
        print(f'Redis error: {e}')
    return

def update_donation(donor, old_amount, new_amount):
    """ delete donation: complex logic:
        -identify if donor exists
        -create local list of all donations_data
        -check if donation exists
        -remove all the donations from redis and reload the list except deleted
    """
    try:
        log.info('Step: connect to Redis')
        log.info('Step: delete donation to Redis')
        don=[]
        old_amount=str(old_amount)
        new_amount=str(new_amount)
        if r.exists(donor):
            for i in range(0, r.llen(donor)):
                don.append(r.lindex(donor, i))
            if old_amount in don:
                don.remove(old_amount)
                don.append(new_amount)
                for i in range(0, r.llen(donor)):
                    r.lpop(donor)
                for i in don:
                    r.rpush(donor,i)
    except Exception as e:
        print(f'Redis error: {e}')
    return

def delete_donor(donor):
    """ delete donor: complex logic:
        -identify if donor exists
        -check if donation exists
        -if there are no donations remove from redis
    """
    try:
        log.info('Step: connect to Redis')
        log.info('Step: delete donor from Redis')
        don=[]
        if r.exists(donor):
            for i in range(0, r.llen(donor)):
                don.append(r.lindex(donor, i))
            if don[0]=='0':
                r.lpop(donor)
        donor_data=donor+id
        if r.exists(donor_data):
            for i in range(0, r.llen(donor_data)):
                r.lpop(donor_data)
    except Exception as e:
        print(f'Redis error: {e}')
    return

def donor_totals():
    """ return the totals in a list"""
    try:
        ls=[]
        for k, v in donors_dict().items():
            v=[float(i) for i in v]
            s=(k,sum(v), len(v), sum(v)/len(v))
            ls.append(s)
    except Exception as e:
            print(f'Redis error: {e}')
    return ls

def donors_list():
    """ return the totals in a list"""
    try:
        ls=[]
        for k, v in donors_dict().items():
            ls.append(k)
    except Exception as e:
            print(f'Redis error: {e}')
    return ls


def donors_dict():
    """ transform the database in a dictionary and return donations"""
    try:
        log.info('Step: connect to Redis')
        log.info('Step: return donor data from Redis')
        donors_donations=defaultdict(list)
        donors_data=defaultdict(list)
        for k in r.keys('*'):
            lst=[]
            for i in range(0, r.llen(k)):
                lst.append(r.lindex(k, i))
            if not k.find(id)>0:
                donors_donations[k]=lst
    except Exception as e:
        print(f'Redis error: {e}')
    return donors_donations

def donors_data_dict():
    """ transform the database in a dictionary and return donor data"""
    try:
        log.info('Step: connect to Redis')
        log.info('Step: return donor data from Redis')
        donors_donations=defaultdict(list)
        donors_data=defaultdict(list)
        for k in r.keys('*'):
            lst=[]
            for i in range(0, r.llen(k)):
                lst.append(r.lindex(k, i))
            if k.find(id)>0:
                donors_data[k]=lst
    except Exception as e:
        print(f'Redis error: {e}')
    return donors_data

def database_erase():
    """
        uses non-presistent Redis only (as a cache)
    """
    try:
        log.info('Step: remove database Redis')
        r.flushdb()

    except Exception as e:
        print(f'Redis error: {e}')
    return

if __name__ == '__main__':
    #setup_database()
    pass
