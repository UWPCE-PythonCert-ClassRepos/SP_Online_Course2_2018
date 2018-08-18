"""
    module that will login to the various demonstration databases consistently
"""

from configparser import ConfigParser
from pathlib import Path
import pymongo
import redis
from neo4j.v1 import GraphDatabase, basic_auth

import utilities

log = utilities.configure_logger('default', '../logs/login_databases_dev.log')
config_file = Path(__file__).parent.parent / '.config/config.ini'
parser = ConfigParser()

def login_mongodb_cloud():
    log.info('Here is where we use the connect to mongodb.')
    log.info('Note use of f string to embed the user & password (from the tuple).')
    try:
        parser.read(config_file)
        user = parser.get('mongodb_cloud', 'user')
        pw = parser.get('mongodb_cloud', 'pw')


    except Exception as e:
        print(f'error: {e}')
    client = pymongo.MongoClient(f'mongodb+srv://{user}:{pw}@cluster0-rrxxf.mongodb.net/test?retryWrites=true')
    return client


def login_redis_cloud():
    """
        connect to redis and login
    """
    try:
        parser.read(config_file)
        host = parser.get('redis_cloud', 'host')
        port = parser.get('redis_cloud', 'port')
        pw = parser.get('redis_cloud', 'pw')
        #r = redis.StrictRedis(host=host, port=port, password=pw, decode_responses=True)
        #return r
    except Exception as e:
        print(f'error: {e}')

    log.info('Here is where we use the connect to redis.')

    try:
        r = redis.StrictRedis(host=host, port=port, password=pw, decode_responses=True)

    except Exception as e:
        print(f'error: {e}')

    return r


def login_neo4j_cloud():
    """
        connect to neo4j and login

    """

    log.info('Here is where we use the connect to neo4j.')
    log.info('')

    parser.read(config_file)

    graphenedb_user = parser.get('neo4j_cloud', 'user')
    graphenedb_pass = parser.get('neo4j_cloud', 'pw')
    graphenedb_url = 'bolt://hobby-jbdnkabhhhgngbkejjhlembl.dbs.graphenedb.com:24786'
    driver = GraphDatabase.driver(graphenedb_url,
                                  auth=basic_auth(graphenedb_user, graphenedb_pass))
    return driver
if __name__ == '__main__':
    login_redis_cloud()