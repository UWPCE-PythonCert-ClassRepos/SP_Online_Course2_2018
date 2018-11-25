"""
    module that will login to the various demonstration databases consistently
"""

import configparser
from pathlib import Path
import pymongo
pymongo.__version__
import redis
from neo4j.v1 import GraphDatabase, basic_auth
import urllib.parse
import ssl

import utilities

log = utilities.configure_logger('default', '../logs/login_databases_dev.log')
config_file = Path(__file__).parent / '.config/config.ini'
config = configparser.ConfigParser()


def login_mongodb_cloud():
    """
        connect to mongodb and login
    """

    log.info('Here is where we use the connect to mongodb.')
    log.info('Note use of f string to embed the user & password (from the tuple).')
    try:
        config.read(config_file)
        user = config['mongodb_cloud']['user']
        pw = config['mongodb_cloud']['pw']
        user1 = urllib.parse.quote_plus(user)
        pw1 = urllib.parse.quote_plus(pw)
        log.info(f'printing user and pw: {user1}, {pw1}')
        pw1 = 'Bostoneastboston99*'

    except Exception as e:
        print(f'error: {e}')


    client = pymongo.MongoClient(f'mongodb://stasaki:Bostoneastboston99%2A@cluster0-shard-00-00-ez67j.mongodb.net:27017,cluster0-shard-00-01-ez67j.mongodb.net:27017,cluster0-shard-00-02-ez67j.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true')
    #client = pymongo.MongoClient(f'mongodb://stasaki:Bostoneastboston99*@cluster0-shard-00-00-ez67j.mongodb.net:27017,cluster0-shard-00-01-ez67j.mongodb.net:27017,cluster0-shard-00-02-ez67j.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true')

    '''
    client = pymongo.MongoClient(f'mongodb://{user1}:{pw1}'
                                 '@cluster0-shard-00-00-maquj.mongodb.net:27017,'
                                 'cluster0-shard-00-01-maquj.mongodb.net:27017,'
                                 'cluster0-shard-00-02-maquj.mongodb.net:27017/test'
                                 '?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin')
    '''
    return client


def login_redis_cloud():
    """
        connect to redis and login
    """
    try:
        config.read(config_file)
        host = config['redis_cloud']['host']
        port = config['redis_cloud']['port']
        pw = config['redis_cloud']['pw']


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

    config.read(config_file)

    graphenedb_user = config['neo4j_cloud']['user']
    graphenedb_pass = config['neo4j_cloud']['pw']
    graphenedb_url = 'bolt://hobby-mdmnpcemepongbkegnfnnfbl.dbs.graphenedb.com:24786'
    driver = GraphDatabase.driver(graphenedb_url,
                                  auth=basic_auth(graphenedb_user, graphenedb_pass))

    return driver
