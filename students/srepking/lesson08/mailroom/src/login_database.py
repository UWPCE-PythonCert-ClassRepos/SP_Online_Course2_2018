"""
    module that will login to the various demonstration databases consistently
"""

import configparser
from pathlib import Path
import pymongo
import redis
from neo4j import GraphDatabase, basic_auth

import utilities

log = utilities.configure_logger('default', '../logs/login_databases_dev.log')
config_file = Path(__file__).parent.parent / '.config/config.ini'
#config_file = 'config.ini'
#log.info('Print config_file to make sure it is found.')
#log.info(f'{config_file}')
config = configparser.ConfigParser()
config.read(config_file)
#log.info(f'Print config.read.{config.read(config_file)}')
#log.info(f'Print user name in mongodb config file.{config["mongodb_cloud"]["user"]}')

def login_mongodb_cloud():
    """
        connect to mongodb and login
    """

    log.info('Here is where we use the connect to mongodb.')
    log.info('Note use of f string to embed the user & password (from the tuple).')
    try:
        config.read(config_file)
        user = config["mongodb_cloud"]["user"]
        pw = config["mongodb_cloud"]["pw"]

    except Exception as e:
        log.info('Getting Exception reading config file.')
        print(f'error: {e}')

    try:
        client = pymongo.MongoClient(f'mongodb://{user}:{pw}@'
                                 f'cluster0-shard-00-00-yorqy.mongodb.'
                                 f'net:27017,cluster0-shard-00-01-yorqy.'
                                 f'mongodb.net:27017,cluster0-shard-00-02-'
                                 f'yorqy.mongodb.net:27017/test?ssl=true&'
                                 f'replicaSet=Cluster0-shard-0&authSource='
                                 f'admin&retryWrites=true')

        return client

    except Exception as e:
        log.info('Error connecting to MongoClient')

def login_redis_cloud():
    """
        connect to redis and login
    """
    try:
        config.read(config_file)
        host = config["redis_cloud"]["host"]
        port = config["redis_cloud"]["port"]
        pw = config["redis_cloud"]["pw"]


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

    graphenedb_user = config["neo4j_cloud"]["user"]
    graphenedb_pass = config["neo4j_cloud"]["pw"]
    graphenedb_url = 'bolt://hobby-fpbonjmgjfpbgbkebmjlndcl.dbs.graphenedb.com:24787'
    driver = GraphDatabase.driver(graphenedb_url,
                                  auth=basic_auth(graphenedb_user, graphenedb_pass))

    return driver
