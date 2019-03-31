import learn_data
import logging
import login_database
import utilities
import pprint
from collections import defaultdict
from copy import deepcopy
from pymongo import MongoClient
import pymongo

log = utilities.configure_logger('default', './logs/mongodb_donor.log')

client=login_database.login_mongodb_cloud()
log.info('Step 1: We are going to use a database called dev')
log.info('But if it doesnt exist mongodb creates it')
db = client['dev']
log.info('And in that database use a collection called donation')
log.info('If it doesnt exist mongodb creates it')
donations = db['donations']

def setup_database():
    donation_database = learn_data.donation_data()
    with login_database.login_mongodb_cloud() as client:
        log.info('Step 2: Now we add data from the dictionary above')
        db = client['dev']
        donations = db['donations']
        donations.insert_many(donation_database)
        result = donations.create_index([('name', pymongo.ASCENDING)],
                                   unique=True)
    return

def add_donor(donor):
    with login_database.login_mongodb_cloud() as client:
        db = client['dev']
        donations = db['donations']
        db.donations.insert({'name':donor, 'donation':[]})
    return

def add_donation(donor,amount):
    with login_database.login_mongodb_cloud() as client:
        db = client['dev']
        donations = db['donations']
        temp = donations.find_one({'name':donor})
        #print (temp['_id'],temp['donation'])
        if not temp:
            donations.insert({'name': donor,'donation': [amount]})
        else:
            id=temp["_id"]
            orig_list=temp['donation']
            temp_list  = deepcopy(orig_list)
            temp_list.append(amount)
            donations.remove({'name':donor})
            donations.insert({'name': donor,'donation': temp_list})
    return

def delete_donation(donor,amount):
    with login_database.login_mongodb_cloud() as client:
        db = client['dev']
        donations = db['donations']
        temp = donations.find_one({'name':donor})
        temp_list = temp['donation'].copy()
        if amount in temp_list:
            temp_list.remove(amount)
            donations.update_one({'name':donor},{'$set': {'donation': temp_list}})
            return True
        else:
            return False

def update_donation(donor, old_amount, new_amount):
    with login_database.login_mongodb_cloud() as client:
        db = client['dev']
        donations = db['donations']
        temp = donations.find_one({'name':donor})
        temp_list = temp['donation'].copy()
        if old_amount in temp_list:
            temp_list.remove(old_amount)
            temp_list.append(new_amount)
            donations.update_one({'name':donor},{'$set': {'donation': temp_list}})
            return True
        else:
            return False

def delete_donor(donor):
    with login_database.login_mongodb_cloud() as client:
        db = client['dev']
        donations = db['donations']
        try:
            temp = donations.find_one({'name':donor})
            if temp['name']==donor and len(temp['donation'])==0:
                donations.remove({'name':donor})
                return True
        except Exception as e:
            log.info('Error deleting donor')
            log.info(e)
            return False

def donor_totals():
    """ return the totals in a list"""
    with login_database.login_mongodb_cloud() as client:
        db = client['dev']
        donations = db['donations']
        temp = donations.find()
        ls=[]
        for t in temp:
            if len(t['donation'])>0:
                s=(t['name'],
                sum(t['donation']),
                len(t['donation']),
                sum(t['donation'])/len(t['donation']))
            else:
                s=(t['name'],0,0,0)
            ls.append(s)
    return ls

def donors_dict():
    """ transform the database in a dictionary"""
    with login_database.login_mongodb_cloud() as client:
        db = client['dev']
        donations = db['donations']
        temp = donations.find()
        new = defaultdict(list)
        for t in temp:
            new[t['name']]=t['donation']
    return new

def donors_list():
    """ return donor list"""
    with login_database.login_mongodb_cloud() as client:
        db = client['dev']
        donations = db['donations']
        temp = donations.find()
        lst=[]
        for t in temp:
            lst.append(t['name'])
    return lst

def database_erase():
    """ clean up"""
    client.drop_database('dev')
    return

if __name__ == '__main__':
    pass
