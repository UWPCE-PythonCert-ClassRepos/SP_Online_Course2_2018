"""
    module that will login to the various demonstration databases consistently
"""

import configparser
import utilities
import pymongo
import redis
from neo4j.v1 import GraphDatabase, basic_auth
from pathlib import Path


log = utilities.configure_logger('default', '../logs/login_databases_dev.log')
config_file = 'config.ini'
config = configparser.ConfigParser()


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
        print(f'error: {e}')
        
    client = pymongo.MongoClient(f'mongodb://ldconejo:test01@cluster0-shard-00-00-maquj.mongodb.net:27017,cluster0-shard-00-01-maquj.mongodb.net:27017,cluster0-shard-00-02-maquj.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true')
    
    return client


def login_redis_cloud():
    """
        connect to redis and login
    """
    try:
        #log.info('Trying to log in to redis_cloud...')
        config.read(config_file)
        host = config["redis_cloud"]["host"]
        port = config["redis_cloud"]["port"]
        pw = config["redis_cloud"]["pw"]
        


    except Exception as e:
        print(f'error: {e}')

    log.info('Here is where we use the connect to redis.')

    try:
        #log.info('passing host, port, pw')
        r = redis.Redis(host=host, port=port, password=pw)
        

    except Exception as e:
        log.info('There is an error...')
        print(f'error: {e}')

    return r


def login_neo4j_cloud():
    """
        connect to neo4j and login

    """

    #log.info('Here is where we use the connect to neo4j.')
    #log.info('')

    config.read(config_file)
    #log.info('Read the config_file')

    graphenedb_user = config["neo4j_cloud"]["user"]
    #log.info('Read the user name')
    graphenedb_pass = config["neo4j_cloud"]["pw"]
    #log.info('Read the pw')
    graphenedb_url = 'bolt://hobby-aogldnogbdekgbkeanmkpkbl.dbs.graphenedb.com:24786'
    driver = GraphDatabase.driver(graphenedb_url, 
            auth=basic_auth(graphenedb_user, graphenedb_pass))
    #log.info('Return the driver to the caller...')
    return driver

#if __name__ == '__main__':
    #login_mongodb_cloud()
    #login_redis_cloud()
    #login_neo4j_cloud()